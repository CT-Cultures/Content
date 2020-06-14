# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:04:07 2019

@author: VX
"""
# 保存电影数据分析函数
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

######################################################################
class Registration(object):
 
    def __init__(self):
        """
        """
        super(Registration, self).__init__()
        
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        
        # 电影备案立项网址
        self.url_reg = "http://dy.chinasarft.gov.cn/html/www/catalog/0129dffcccb1015d402881cd29de91ec.html"
        
        # folder for saving records, relative
        self.path_records = 'records'
        
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
        records.to_csv(path_file, encoding='utf-8')
        print('file saved to: ', filename, '.csv')

        
##########
    def links_of_pages(self) -> pd.DataFrame:
        """This function grabs all landing pages of movie registrations
        @return links_of_pages: pd.DataFrame
        """
        with urlopen(self.url_reg) as x: 
            html = x.read().decode('utf-8')
        links_of_pages = []
        bsObj = BeautifulSoup(html, 'html5lib')
        for item in bsObj.find_all(href=re.compile("pageIndex")):
           links_of_pages += (self.url_base + item.get("href"),)
        links_of_pages = links_of_pages[0:-2]# 删除最后两个链接：下一页与最后一页
        
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])
            
        return links_of_pages

########## 
    def links_of_publications(self, 
                              filename: str = "PubThreatricalRegistration_links_allpublishes", 
                              savefile: bool = False) -> pd.DataFrame:
        """
        @param savefile: bool, whether to save the file to disk
        @return links_of_publications: pd.DataFrame

        """
        links_of_pages = self.links_of_pages()
        links_of_publications = []
        for _, page in links_of_pages.iterrows():
            with urlopen(page['links_of_pages']) as x: 
                html = x.read()   # site has probelm decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find_all(href=re.compile("blueprint.nsp?")):
                links_of_publications += [[self.url_base + item.get("href"), str(item.next_element)]]
        links_of_publications = pd.DataFrame(links_of_publications)
        links_of_publications.columns = ['公示批次链接','名称']
       
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
        return links_of_publications

##########
    def links_of_new_publications(self, 
                                  filename: str = "PubThreatricalRegistration_links_allpublishes",
                                  update_records: bool = False) -> pd.DataFrame:
        """
        This functions finds the links to new publications
        @param update_records: bool, whether to updated the saved records
        @return records_new: pd.DataFrame
        """
       
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', index_col=0, encoding='utf-8')
        else:
            records_existing = pd.DataFrame(columns = ['公示批次链接','名称'])
            
        # 网上获取最新
        records_latest = self.links_of_publications()
        records_new = records_latest[~records_latest['公示批次链接'].isin(records_existing['公示批次链接'])]

        if update_records:
            self.save_records(records_latest, filename, backup=True)
            print(filename + '.csv updated.')
        
        return records_new

##########    
    def links_of_registrations(self, 
                               links_of_publications: pd.DataFrame, 
                               filename: str = "PubThreatricalRegistration_links_allregistrations",
                               savefile: bool = False) -> pd.DataFrame:
        """
        This functions finds the links of publications give links of pages

        Parameters
        ----------
        links_of_publications : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "PubThreatricalRegistration_links_allregistrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        pd.DataFrame

        """

        links_of_registrations = []
        url_part_blueprint = '/shanty.deploy/blueprint.nsp?'
        templateId = 'templateId=012a2e051030004740284c812a2d62df'     
        pattern_id = re.compile("id=.*?&")  # 定义查找id的规律 
        for _, publication in links_of_publications.iterrows():
            with urlopen(publication['公示批次链接']) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                title_publish = bsObj.find(class_="heading").get_text()
#                print(title_publish)
                dt_publish = bsObj.find(class_="time").get_text().lstrip(u' 【发布时间】:').rstrip(' ')
#                print(dt_publish)
                for item in bsObj.find_all(["table", "a"], onclick=True):
#                    print(item)
#                    html_review +=(str(item),)
                    str_item = re.sub('\n.*?\n', '', str(item)) # clean spaces and breaks
                    if pattern_id.search(str_item) != None:
                        str_id = pattern_id.search(str_item)[0]
                        clean_char = re.sub("\"", '', str_id)
                        str_id = clean_char
                    else:
                        str_id = '__NO_ID__'
                        print(str_id, ": ")
                        print(title_publish)
                        print(str(len(links_of_registrations)), ": ")
                        print("str(item): " + str(item))
                        print("str_item: " + str_item)
                    url_link_reg = self.url_base + url_part_blueprint + str_id + templateId
#                    print(url_link_reg)
                    links_of_registrations += [[dt_publish, title_publish, url_link_reg]]
        if len(links_of_registrations) != 0:
            links_of_registrations = pd.DataFrame(links_of_registrations)
            links_of_registrations.columns = ['公示日期', '公示批次名称', '备案详细页链接']
        else:
            links_of_registrations = pd.DataFrame(columns = ['公示日期', '公示批次名称', '备案详细页链接'])
        
        if savefile:
            self.save_records(links_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')

        return links_of_registrations
 
##########
    def links_of_new_registrations(self, 
                                   filename: str = "PubThreatricalRegistration_links_allregistrations" ,
                                   comprehensive: bool = False,
                                   update_records: bool = False) -> pd.DataFrame:
        """
        This functions gets the links of new registrations not currently in record.

        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "PubThreatricalRegistration_links_allregistrations".
        comprehensive : bool, optional
            DESCRIPTION. The default is False. 
                         [True], will fetch page and publications links from scratch to construct records
                         [False], willrerun use differences from links_of_publications to fill in new records
        update_records : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_new_registrations : TYPE
            DESCRIPTION.

        """
        # Import Existing Records
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', index_col=0, encoding='utf-8')
        else:
            records_existing = pd.DataFrame(columns = ['公示日期', '公示批次名称', '备案详细页链接'])  
            
            
        if comprehensive:
            links_of_publications = self.links_of_publications(savefile=update_records)
            records_latest = self.links_of_registrations(links_of_publications, savefile=update_records)
            records_new = records_latest[~records_latest['备案详细页链接'].isin(records_existing['备案详细页链接'])]
        else:
            links_of_new_publications = self.links_of_new_publications(update_records=update_records)
            records_new = self.links_of_registrations(links_of_new_publications, savefile=update_records)
            records_latest = pd.concat([records_new, records_existing], axis=0, ignore_index=True)
             
        if update_records:
            self.save_records(records_latest , filename, backup=True)
            print(filename + '.csv updated.')
            
        return records_new

##########
    def contents_of_registrations(self, 
                                  links_of_registrations: pd.DataFrame, 
                                  filename: str = "PubTheatricalRegistration_info_allregistrations",
                                  savefile: bool = False) -> pd.DataFrame:

        """
        This functions grabs the contents of film registrations

        Parameters
        ----------
        links_of_registrations : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "PubTheatricalRegistration_info_allregistrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        pd.DataFrame
            DESCRIPTION.

        """
        contents_of_registrations = []
        for _, link in links_of_registrations.iterrows():
            with urlopen(link['备案详细页链接']) as x:
                html = x.read()
            bsObj_reg = BeautifulSoup(html, 'html.parser')
            table = bsObj_reg.find("table", class_="form") # 读取信息表
            tb_row_second = list()
            tb_row_third= list()                  
            for item in table.find("tr").find_next_sibling("tr").find_all("td"):
                tb_row_second.append(item.get_text().rstrip('\xa0'))
#            print(tb_row_second)
            for item in table.find("tr").find_next_sibling("tr").find_next_sibling("tr").find_all("td"):
                tb_row_third.append(item.get_text().lstrip('\n梗概：').rstrip('\n'))
            tb_row_third.append(link[0])
            tb_row_third.append(link[1])
            tb_row_third.append(link[2])
#            print(tb_row_third)
            info_reg = tb_row_second + tb_row_third
#            print(tb_info_reg)
            contents_of_registrations += [info_reg]
#        print("Total number of " + str(len(info_allregistrations)-1) + " registration info scrapped from web.")
        if len(contents_of_registrations) != 0:
            contents_of_registrations = pd.DataFrame(contents_of_registrations)
            contents_of_registrations.columns = ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接']
        else:
            contents_of_registrations = pd.DataFrame(columns=
                                         ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接'])

        if savefile:
            self.save_records(contents_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
                  
        return contents_of_registrations


##########
    def contents_of_new_registrations(self, 
                                      filename: str = "PubTheatricalRegistration_info_allregistrations",
                                      comprehensive: bool = False,
                                      update_records: bool = False) -> pd.DataFrame:
        """
        This functions gets the contents of new registrations

        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "PubTheatricalRegistration_info_allregistrations".
        update_records : bool, optional
            DESCRIPTION. The default is False. If True, will update:
                            links_of_new_publications,
                            links_of_new_registrations,
                            contents_of_new_registrations

        Returns
        -------
        DataFrame
            DESCRIPTION.

        """
        # Import Existing Records
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', index_col=0, encoding='utf-8')
        else:
            records_existing = pd.DataFrame(columns = ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接'])  
        
        if comprehensive:
            links_of_publications = self.links_of_publications(savefile=update_records)
            links_of_registrations = self.links_of_registrations(links_of_publications, savefile=update_records)
            records_latest = self.contents_of_registrations(links_of_registrations, savefile=update_records)
            records_new = records_latest[~records_latest['备案立项号'].isin(records_existing['备案立项号'])]
        else:
            links_of_new_registrations = self.links_of_new_registrations(update_records=update_records)
            records_new = self.contents_of_new_registrations(links_of_new_registrations)
            records_latest = pd.concat([records_new, records_existing], axis=0, ignore_index=True)
            
        if update_records:
              self.save_records(records_latest, filename, backup=True)
              print("Contents of Registrations updated: ", + len(links_of_new_registrations ), " record(s).")

        return records_new
    
    def Registration_Records(self, 
                             filename: str = "PubTheatricalRegistration_info_allregistrations",
                             regid: bool = True,
                             title: bool = True,
                             regco: bool = True,
                             writer: bool = True,
                             status: bool = True,
                             regregion: bool = True,
                             summary: bool  = True,
                             pubdate: bool = True,
                             pubname: bool = True,
                             publink: bool = True,
                             correct_typos: bool = True
                             ) -> pd.DataFrame:
        
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', index_col=0, encoding='utf-8')
        else:
            links_of_publications = self.links_of_publications()
            links_of_registrations = self.links_of_registrations(links_of_publications)
            
        records = pd.read_csv(filename, '')
        
        return records
            
        
##########
    def correct_typos(self, 
                         contents_of_registrations: pd.DataFrame) -> pd.DataFrame:
        """This functions corrects typos in the registration, all picked out manually,
        future corrections can be updated here.
        @param contents_of_registrations: pd.DataFrame
        @return contents_of_registrations: pd.DataFrame
        """
        pubtitle_error_corrector = {
         '国家新闻出版广电总局电影局关于2011年10月全国电影剧本（梗概）备案、立项公示的通知':
         '国家新闻出版广电总局电影局关于2015年04月（上旬）全国电影剧本（梗概）备案、立项公示的通知',
         
         '广电总局电影局关于2017年11月（下旬）全国电影剧本（梗概）备案、立项公示的通知':
         '广电总局电影局关于2011年11月（下旬）全国电影剧本（梗概）备案、立项公示的通知',
         
         '广电总局电影局关于2011年06月（下旬）全国电影剧本（梗概）备案、立项公示的通知':
         '广电总局电影局关于2012年06月（下旬）全国电影剧本（梗概）备案、立项公示的通知'}
        
        contents_of_registrations.apply(lambda x: pubtitle_error_corrector[x] if x in pubtitle_error_corrector else x)

        return contents_of_registrations
