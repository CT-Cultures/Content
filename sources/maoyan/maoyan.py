# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:18:10 2019

@author: VSurfacePro3
"""
#%%
import os
import datetime

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
#import lxml
import re
import pandas as pd
#%%
class Maoyan(object):
##########   
    def __init__(self):
        if not self:
            raise ValueError
        self.mobile_emulation = { 
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
            }
        self.chromeoptions = webdriver.ChromeOptions()
        self.chromeoptions.add_argument('--headless')
        self.chromeoptions.add_argument('--no-sandbox')
        self.chromeoptions.add_argument('--disable-dev-shm-usage')
        self.chromeoptions.add_argument('--save-page-as-mhtml')
        self.chromeoptions.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.driver = webdriver.Chrome(options = self.chromeoptions)
        self.url_base = 'https://m.maoyan.com'
        self.landing_page = None
        
        self.path_records = 'records'
        self.path_searches = 'searches'

##########        
    def save_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to json files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '/' + filename + '.json'
        path_file_bk = self.path_records + '/backup/' + filename + appendix_dt + '.json'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_json(path_file)
        print('file saved to: ' + filename + '.json with a total of ', 
              records.shape[0], ' records.')

##########         
    def save_search(self, df_search: pd.DataFrame) -> None:
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))
        path_file = self.path_searches + '/' + 'search_{}.json'.format(appendix_dt)
        df_search.to_json(path_file)
        print('search result saved to: {}'.format(path_file),
              ' with {} records'.format(df_search.shape[0])
        )
##########      
    def update_records(self, df_search: pd.DataFrame):
        """
        This function updates

        Parameters
        ----------
        df_search : TYPE
            DESCRIPTION.

        Returns
        -------
        df_latest : TYPE
            DESCRIPTION.

        """
        fn = 'records_maoyan'
        if os.path.isfile(self.path_records + '//' + fn):
           self.records_maoyan = pd.read_json(
               self.path_records + '//' + fn)
        else:
            self.records_maoyan = pd.DataFrame(
                columns=['片名', 'fid', '主演', '上映日期'])
        
        df_new = df_search[~df_search['fid'].isin(self.records_maoyan['fid'])]

        df_latest = pd.concat([self.records_maoyan, df_new], ignore_index=True)
        
        """ WIP, update release date with each new search
        df_existed = df_search[df_search['fid'].isin(self.records_maoyan['fid'])]
        def update_release_dt(row):
            item = df_existed[df_existed.fid == 'fid', ['fid', '上映日期']]
            if item.empty: 
                return row['上映日期']
            return item['上映日期'].iloc[0]
            
        df_latest['上映日期'] = df_latest[['fid', '上映日期']].apply(
            update_release_dt, axis=1)
        """
        self.save_records(df_latest, fn)
        
        return df_latest
        
##########           
    def get_app_landing_page(self):
        self.driver.get(self.url_base)
        WebDriverWait(self.driver, 5)
        self.landing_page = self.driver.page_source
        return self.landing_page
##########       
    def on_screen(self):
        if not self.landing_page:
            self.landing_page = self.get_app_landing_page()
        soup = BeautifulSoup(self.landing_page, features='lxml')
        
        items = soup.find_all('div', class_="mb-outline-b content-wrapper")
                                  #('div', class_="main-block")
        ls = []
        for f in items:
            d = {}
            
            title = f.find('div', class_=re.compile('title line-ellipsis'))
            if title: d['片名'] = title.text
            else: d['片名'] = None
            
            actor = f.find('div', class_=re.compile('actor line-ellipsis'))
            if actor: d['主演'] = actor.text.lstrip('主演: ').split(',')
            else: d['主演'] = None
                
            dt_release = f.find('div', class_=re.compile('show-info line-ellipsis'))
            if dt_release: d['上映日期'] = dt_release.text.split(' ')[0]
            else: d['上映日期'] = None
            
            fid = f.find('div', class_=re.compile('button-block'))
            if fid: d['fid'] = fid.attrs['data-id']
            else: d['fid'] = None
            
            want_to_see = f.find('span', class_='person')
            if want_to_see: d['想看'] = want_to_see.text
            else: d['想看'] = None
            
            ls.append(d)
            
        df = pd.DataFrame.from_dict(ls)
        self.save_search(df)
        self.update_records(df)
        
        return df
##########       
    def search(self, str_item):
        url_search = self.url_base + '/' + str_item        
        self.driver.get(url_search)
        self.driver.implicitly_wait(2)
        page = self.driver.page_source
        return page    
##########      
    def search_for_content(self, str_item):
        page = self.search(str_item)
        content = self.parse_content(page)
        return content
    
    def parse_content(self, page):
        bsObj = BeautifulSoup(page, 'html5lib')
        content = bsObj.find(attrs={"name": "description"})
        if content != None:
            content = content.get("content")
        else:
            content = ''
        return content
    
    def get_release_date(self, page):
        bsObj = BeautifulSoup(page, 'html5lib')
        item = bsObj.find('dt', text=re.compile('上映时间'))
        if item != None:
            item = item.next_sibling.next_sibling.text.strip()
        return item 
 
    def get_talents(self, page):
        bsObj = BeautifulSoup(page, 'html5lib')
        item = bsObj.find('dt', text=re.compile('主演'))
        if item != None:
            item = item.next_sibling.next_sibling.text.strip()
        return item
    
    def get_principal_photography_date(self, page):
        bsObj = BeautifulSoup(page, 'html5lib')
        item = bsObj.find('dt', text=re.compile('拍摄日期'))
        if item != None:
            item = item.next_sibling.next_sibling.text.strip()
        return item 
        
    def get_director(self, page):
        bsObj = BeautifulSoup(page, 'html5lib')
        item = bsObj.find('dt', text=re.compile('导演'))
        if item != None:
            item = item.next_sibling.next_sibling.text.strip()
        return item
    
    def batchsearch_for_content(self, list_str_items):
        list_title_content = []
        for item in list_str_items:
            content = self.search_for_content(item)
            list_title_content = [item, content]
        return list_title_content
