# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:03:16 2020

@author: CT Cultures
"""
#%%
# Load Standard Library
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
from urllib.error import HTTPError
import re
import numpy as np
import pandas as pd

import datetime
from pathlib import Path
import os

# Load from Local
#from IO_Storage import File

######################################################################
class GetRelease(object):
    
    def __init__(self):
        
        super(GetRelease, self).__init__()
        
        # 中国电影电子政务平台网址
        self.url_base = "http://www.chinafilm.gov.cn"
        
        # 电影电子政务平台备案公示网址
        self.url_release = "http://www.chinafilm.gov.cn/chinafilm/channels/168.shtml"
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()
    
    ##########        
    def save_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to csv files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '//' + filename + '.csv'
        path_file_bk = self.path_records + '//backup//' + filename + appendix_dt + '.csv'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_csv(path_file, encoding='utf-8-sig', index=False)
        print('file saved to: ' + filename + '.csv')
    
    ##########  
    
    def links_of_pages(self,
                       filename: str = "links_of_pages_release",
                       savefile: bool = False) -> pd.DataFrame:
        """
        
        从 电影局官网 抓取 公示分页 的链接
        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "links_of_pages_release".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_pages : TYPE
            DESCRIPTION.

        """
    

        try:
            with urlopen(self.url_release) as x: html = x.read().decode('utf-8')
        except HTTPError as e:
            print(e)
        bsObj = BeautifulSoup(html, 'html5lib')
        links_of_pages = [self.url_release]
        for item in  bsObj.find_all(attrs={"class": "page_a"}):
           links_of_pages.append(self.url_base + item.get("href"))
           
        links_of_pages = pd.DataFrame(links_of_pages)
        links_of_pages.columns = ['links_of_pages']
        links_of_pages.drop_duplicates(keep='first', inplace=True)
        links_of_pages = links_of_pages[links_of_pages['links_of_pages'] != 'http://www.chinafilm.gov.cnjavascript:;']
        links_of_pages.reset_index(inplace=True, drop=True)
        
        
        if savefile:
            self.save_records(links_of_pages, filename, backup=True)
            
        return links_of_pages
    
    def links_of_publications(self, 
                              links_of_pages: pd.DataFrame = 'default',
                              filename: str = "links_of_publications_release", 
                              savefile: bool = False) -> pd.DataFrame:
        # 从 电影局官网 抓取 公映许可证发放 批次页 的 链接
        if links_of_pages == 'default':
            links_of_pages = self.links_of_pages
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        links_of_publications = []
        
        for _, page in links_of_pages.iterrows():
            with urlopen(page['links_of_pages']) as x: 
                html = x.read()   # site has problem decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find(attrs={"class": "m2ru1 m2ru11"}).find_all('li'):
                title = item.a.span.next.next  # title
                link = self.url_base + item.a.get('href') # link
                dt_publish = item.a.span.next.next.next.next # pubdate
                links_of_publications.append([title, link, dt_publish])
                
                
        if len(links_of_publications) != 0:
            links_of_publications = pd.DataFrame(links_of_publications)
            links_of_publications.columns = ['公示名称', '公映许可证发放公示批次链接', '公示日期']
        else:
            links_of_publications = pd.DataFrame(columns = ['公示名称', '公映许可证发放公示批次链接', '公示日期'])
            
                  
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
            
        return links_of_publications
        
    def contents_of_publications(self, 
                                 links_of_publications: pd.DataFrame,
                                 filename: str = "contents_of_publications_release", 
                                 savefile: bool = False) -> pd.DataFrame:

        #从 电影局官网 抓取 公映许可证发放批次页，从中清理出内容信息
        if len(links_of_publications) == 0:
            contents_of_publications = pd.DataFrame([])
            contents_of_publications.columns = ['公映许可证发放公示批次链接', '公示日期']
        
        for _, item in links_of_publications.iterrows():
            with urlopen(item['公映许可证发放公示批次链接']) as x：
                html = x.read()
                bsObj= BeautifulSoup(html, 'html5lib')
      
        return contents_of_publications
    
class UpdateRelease(object):
    
    def __init__(self):
        super(UpdateRelease, self).__init__()
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        # 电影备案立项网址
        self.url_release = "http://dy.chinasarft.gov.cn/html/www/catalog/012996c2a84002724028815629965e99.html"
        self.path_records = 'records'

    def links_of_newpublications(self, savefile=False):
        GRS = GetRelease()
        # 打开现有存档
        filename = "PubThreatricalRelease_links_allpublishes"
        heading_links_publications = ['公映许可证发放公示批次链接', '公示日期']
        reader = File()
        filepath = Path(self.path_results + "\\" + filename + ".csv")
        records_existing = reader.open_to_list_of_list(filepath)
        if heading_links_publications == records_existing[0]:
            records_existing = records_existing[1:len(records_existing)] #saved records shall have heading, remove heading
        # 网上获取最新
        records_latest = GRS.links_of_publications()
        len_diff= len(records_latest) - len(records_existing)
        list_links_newpublications = []
        if len_diff != 0:
            index = 0
            while index < len_diff:
                list_links_newpublications += [records_latest[index]]
                index = index + 1
            if savefile:
                filename = "PubThreatricalRelease_links_allpublishes"
                reader = File()
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing = reader.open_to_list_of_list(filepath)
                if heading_links_publications == records_existing[0]:
                    records_existing = records_existing[1:]
                already_in_record = list(filter(lambda x:x == list_links_newpublications[0], records_existing))
                if not already_in_record:
                    records_joined = [heading_links_publications] + list_links_newpublications + records_existing
                    writer = File()
                    writer.write_to_cvs_wbk(records_joined, self.path_records, filename)               
        return list_links_newpublications
    
     ##########           
    def contents_of_newpublications(self, savefile=False):
        GRS = GetRelease()                
        list_links_newpublications = self.links_of_newpublications()
        list_contents_newpublications  = []
        if len(list_links_newpublications) != 0:
            list_contents_newpublications = GRS.contents_of_publications(list_links_newpublications)
            headings_info_releases = ['编码','公映证号','片名','第一出品单位','批次名称',
                                      '公示批次中的序号','批次链接','发布日期']
            if savefile:
                self.links_of_newpublications(savefile=savefile)
                print("Links of Release Publications updated, added ", + len(list_links_newpublications), " record(s).")   
                filename = "PubThreatricalRelease_info_allreleases"
                reader = File()
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing = reader.open_to_list_of_list(filepath)
                if headings_info_releases == records_existing[0]:
                    records_existing = records_existing[1:]
                if len(list_contents_newpublications) != 0:
                    already_in_record = list(filter(lambda x:x == list_contents_newpublications[0], records_existing))
                    if not already_in_record:
                        records_joined = [headings_info_releases] + list_contents_newpublications + records_existing
                        writer = File()
                        writer.write_to_cvs_wbk(records_joined, self.path_records, filename)
                        print("Contents of Release Publications updated, added ", + len(list_contents_newpublications), " record(s).")   
        return list_contents_newpublications
    
