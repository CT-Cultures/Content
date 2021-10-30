# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:03:16 2020

@author: CT Cultures
"""
#%%
# Load Standard Library
# Load Standard Library
import os
#from sys import platform
from urllib.request import Request, urlopen
#from urllib.error import HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup

import re
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import datetime
from datetime import date
from datetime import timedelta

# Load from Local
#from IO_Storage import File

######################################################################
class Release(object):
    
    def __init__(self):
        
        super(Release, self).__init__()
        
        # 中国电影电子政务平台网址
        self.url_base = "http://www.chinafilm.gov.cn"
        
        # 电影电子政务平台备案公示网址
        self.url_release = "http://www.chinafilm.gov.cn/chinafilm/channels/168.shtml"
        
        # url_browser head
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # folder for aving logs, relative
        self.path_logs = 'logs'
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()
        
        self.links_of_publications_existing = pd.DataFrame()
        self.contents_of_releases_existing = pd.DataFrame()
        if os.path.isfile(self.path_records + '//' + 'links_of_publications_releases.json'):
           self.links_of_publications_existing = pd.read_json(
               self.path_records + '//' + 'links_of_publications_releases.json')       

        if os.path.isfile(self.path_records + '//' + 'contents_of_releases.json'):
            self.contents_of_releases_existing = pd.read_json(
                self.path_records + '//' + 'contents_of_releases.json')
    
    ##########        
    def save_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to csv files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) \
            + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '/' + filename + '.json'
        path_file_bk = self.path_records + '/backup/' \
            + filename + appendix_dt + '.json'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_json(path_file)
        print('{} records saved to {}.'.format(
            records.shape[0], path_file))
    
    ##########  
    
    def links_of_pages(self,
                       filename: str = "links_of_pages_releases",
                       savefile: bool = False) -> pd.DataFrame:
        """
        
        从 电影局官网 抓取 公示分页 的链接
        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "links_of_pages_releases".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_pages : TYPE
            DESCRIPTION.

        """

        req = Request(url=self.url_release, headers=self.headers) 
        with urlopen(req) as x: 
            html = x.read().decode('utf-8')
            
        bsObj = BeautifulSoup(html, 'html5lib')
        
        str_total_number_of_pages = bsObj.find(text=re.compile(u'共[0-9]*页'))
        total_number_of_pages = int(str_total_number_of_pages[1:-1])
        links_of_pages = [self.url_release]       
        
        for n in range(2, total_number_of_pages+1):
            links_of_pages.append(self.url_release[:-6] + '_' + str(n) + '.shtml')
        
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])

        if savefile:
            self.save_records(links_of_pages, filename, backup=True)
            
        return links_of_pages
    
    def links_of_publications(self, 
                              links_of_pages: pd.DataFrame = 'default',
                              filename: str = "links_of_publications_releases", 
                              savefile: bool = False) -> pd.DataFrame:
        # 从 电影局官网 抓取 公映许可证发放 批次页 的 链接
        if links_of_pages == 'default':
            links_of_pages = self.links_of_pages
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        links_of_publications = []
        
        for _, page in links_of_pages.iterrows():
            req = Request(url=page['links_of_pages'], headers=self.headers) 
            with urlopen(req) as x: 
                html = x.read().decode('utf-8')   # site has problem decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find_all('a', class_="m2r_a"):
                links_of_publications += [[self.url_base + item.get("href"), str(item.text)[1:]]]
                
                
        if len(links_of_publications) != 0:
            links_of_publications = pd.DataFrame(links_of_publications)
            links_of_publications.columns = ['公示批次链接', '公示名称']
        else:
            links_of_publications = pd.DataFrame(columns = ['公示批次链接', '公示名称'])
            
                  
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
            
        return links_of_publications
        
    def contents_of_releases(self, 
                                 links_of_publications: pd.DataFrame,
                                 filename: str = "contents_of_releases", 
                                 savefile: bool = False) -> pd.DataFrame:

        #从 电影局官网 抓取 公映许可证发放批次页，从中清理出内容信息
        contents_of_releases = []
        for _, publication in links_of_publications.iterrows():
            req = Request(url=publication['公示批次链接'], headers=self.headers) 
            with urlopen(req) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                
                dt_publish = bsObj.find('span', class_='fl').text
                dt_publish = re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]', dt_publish)[0]
                
                table = pd.read_html(html, header=0)[0]
                table['公示批次链接'] = publication['公示批次链接']
                table['公示名称'] = publication['公示名称']
                table['公示日期'] = dt_publish
                
                contents_of_releases.append(table)
                
        if len(contents_of_releases) != 0:
            contents_of_releases = pd.concat([contents_of_releases[i] for i in range(len(contents_of_releases))], ignore_index=True)
        else:
            contents_of_releases.columns = ['序号', '电影类别', '编码', '公映证号', '片名', '第一出品单位']
            
        if savefile:
            self.save_records(contents_of_releases, filename, backup=True)
            print(filename + '.csv updated.')
      
        return contents_of_releases
    
    def update_records(self, 
                       fn_links_of_publications: str = "links_of_publications_releases",
                       fn_contents_of_releases: str = "contents_of_releases",
                       save_update: bool = False
                       ) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        fn_links_of_publications : str, optional
            DESCRIPTION. The default is "links_of_publications_releases".
        fn_contents_of_releases : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        save_update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        # Import Existing Records:
        if os.path.isfile(self.path_records + '//' + fn_links_of_publications + '.json'):
            links_of_publications = pd.read_csv(self.path_records + '//' + fn_links_of_publications + '.json')
        else:
            links_of_publications = self.links_of_publications('empty')
        
            
        if os.path.isfile(self.path_records + '//' + fn_contents_of_releases + '.csv'):
            contents_of_releases = pd.read_csv(self.path_records + '//' + fn_contents_of_releases + '.json')
        else:
            contents_of_releases = self.contents_of_releases(links_of_publications = pd.DataFrame())
        
        links_of_publications_latest = self.links_of_publications()
        
        # Find Records to update