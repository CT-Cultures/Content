# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 19:19:59 2021
CT-Cultures
@author: Herais
"""
#%% Import Global Libraries
import os
import datetime

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import urllib.request


from bs4 import BeautifulSoup
#import lxml
import re
import pandas as pd
#%% Import Common Libraries
from common.utils import DB
#%%
class ZGDYPW(DB):
    
    def __init__(self):
        
        super(ZGDYPW, self).__init__()
        
        # Define Relative Path        
        self.path_records = 'records'
        self.path_searches = 'searches'
        
        # Instantiate Selenium Driver
        self.chromeoptions = webdriver.ChromeOptions()
        self.chromeoptions.add_argument('--headless')
        self.chromeoptions.add_argument('--no-sandbox')
        self.chromeoptions.add_argument('--disable-dev-shm-usage')
        self.chromeoptions.add_argument('--save-page-as-mhtml')
        #self.chromeoptions.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.driver = webdriver.Chrome(options = self.chromeoptions)
        self.url_base = 'https://www.zgdypw.cn/'
        
        # Define Pages on IMDB
        self.landing_page = None
        self.market_page = None


    def __version__(self):
        version = '1.0.0'
        self.__version__ = version
        print('Content-ZGDYPW-{}'.format(version))

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
        records.to_json(path_file, orient='split')
        print('file saved to: ' + filename + '.json with a total of ', 
              records.shape[0], ' records.')
        
    def landing_page(self):
        if not self.landing_page:
            self.driver.get(self.url_base)
            WebDriverWait(self.driver, 10)
            self.landing_page = self.driver.page_source
        return self.landing_page
    
    def get_page_source(self, url, wait=10):
        self.driver.get(url)
        WebDriverWait(self.driver, wait)
        page = self.driver.page_source
        return page
    
    def landing_marketpage(self):
        url = self.url_base + 'sc/scxx/'
        self.driver.get(url)
        WebDriverWait(self.driver, 10)
        self.market_page = self.driver.page_source
        return self.market_page
    
    def links_of_marketpage(self):
        self.market_page = self.landing_marketpage()
        soup = BeautifulSoup(self.market_page, 'lxml')
        str_npages = soup.find('span', class_='fy_cur1').text
        N = int(re.findall('/([0-9]*)页', str_npages)[0])
        links_of_pages = [self.url_base + 'sc/scxx/']
        for i in range(1,N):
            link = self.url_base + 'sc/scxx/index_{}.shtml'.format(i)
            links_of_pages.append(link)
        return links_of_pages
    
    def links_of_releases(self, links_of_marketpage, 
                          return_dict = False):
        ret = {}
        links = []
        pages = []
        for url in links_of_marketpage:
            page = self.get_page_source(url)
            pages.append(page)
            elements_newreleaselink = \
                self.driver.find_elements_by_partial_link_text("新片上映")
                #By.XPATH, "//a[@title='新片上映预报']")
            for ele in elements_newreleaselink:
                links.append(ele.get_attribute('href'))
        
        if return_dict:
            ret['links'] = links
            ret['pages'] = pages
            return ret
        return links
    
    def contents_of_releases(self, 
                             links_of_releases,
                             save=False):
        ls_df = []
        for url in links_of_releases:
            df = self.extract_release_records(url)
            ls_df.append(df)
        
        df = pd.DataFrame()
        if len(ls_df) > 0:
            df = pd.concat(ls_df, ignore_index=True).sort_values(
                'pubdate').reset_index(drop=True)
        
        df = df.drop_duplicates()
        if save:
            self.save_records(df, 'contents_of_releases', backup=True)   
        return df
    

    def extract_release_records(self, url) -> pd.DataFrame:
        page = self.get_page_source(url)
        soup = BeautifulSoup(page, 'lxml')

        keys = ['电影名称', '上映日期', '导演', '主演', '国别/地区', '国别',]
        #<span id="articleTime"><b>发布时间：</b>2021-07-05</span>
        date = soup.find('span', id='articleTime').text
        date = date.lstrip('发布时间：').strip()
        
        #<h3 id="articleTitle">新片上映（2021.08.06-08.14）</h3>
        title = soup.find('h3', id='articleTitle').text.strip()
        title = re.sub(' ', '', title)

        
        ls_df = []
        rec = {}
        for table in soup.find_all('table'):
            j = 0
            for tr in table.find_all('tr'):
                for i, td in enumerate(tr.find_all('td')):
                    if i not in rec:
                        rec[i] = {}
                    if td.img != None:
                        rec[i]['img_remote'] = \
                            '/'.join(url.split('/')[:-1]) + td.img['src'][1:]
                    else:
                        for k in keys:
                            if re.search('{}：'.format(k), td.text):
                                if k == '国别':
                                    rec[i]['国别/地区'] = re.split('{}：'.format(k), td.text)[1].strip('\w+')
                                else:
                                    rec[i][k] = re.split('{}：'.format(k), td.text)[1].strip('\w+')
                    rec[i]['pubtitle'] = title
                    rec[i]['pubdate'] = date
                    rec[i]['publink'] = url
            dfp = pd.DataFrame.from_dict(rec, orient='index')
            ls_df.append(dfp)
            j += 3
            
        df = pd.DataFrame()
        if len(ls_df) > 0:
            df = pd.concat(ls_df, ignore_index=True)
        
        return df
    
    def update_contents_of_releases(self, 
        fn_contents_of_releases: str = "contents_of_releases",
        how:str ='quick',
        save: bool = False
        ) -> pd.DataFrame:
        
        links_of_marketpage_latest = self.links_of_marketpage()
        links_of_releases_latest = self.links_of_releases(
            links_of_marketpage_latest) # List[str]
        
        df_links_of_releases_latest = \
            pd.Series(links_of_releases_latest).rename('publink').to_frame()
        
        contents_of_releases_existing = pd.read_json(
            self.path_records + '/' + fn_contents_of_releases + '.json', orient='split')
        
        
        if how == 'quick':
            
            publications_unique = \
                contents_of_releases_existing['publink'].unique()    
            links_of_releases_new = df_links_of_releases_latest[
                ~df_links_of_releases_latest['publink'].isin(publications_unique)
            ]  
            links_of_releases_latest = None
            contents_of_releases_new = self.contents_of_releases(
                links_of_releases_new)
            
            contents_of_releases_latest = pd.concat(
                [contents_of_releases_new, contents_of_releases_existing],
                ignore_index=True
            ).drop_duplicates().sort_values('pubdate').reset_index(drop=True)
                 
        if how == 'comprehensive':
            contents_of_releases_latest = self.contents_of_releases(
                links_of_releases_latest)
        
        
        if save==True:
            self.save_records(contents_of_releases_latest,
                              fn_contents_of_releases
                              )
            
        return  contents_of_releases_latest
        