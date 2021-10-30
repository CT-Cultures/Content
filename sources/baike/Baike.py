# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:18:10 2019

@author: VSurfacePro3
"""
#%%
#import re
#from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import re

#%%
class Baike(object):

    def __init__(self):
        if not self:
            raise ValueError
        self.chromeoptions = webdriver.ChromeOptions()
        self.chromeoptions.add_argument('--headless')
        self.chromeoptions.add_argument('--no-sandbox')
        self.chromeoptions.add_argument('--disable-dev-shm-usage')
        self.chromeoptions.add_argument('--save-page-as-mhtml')
        self.driver = webdriver.Chrome(options = self.chromeoptions)
        self.url_base = 'https://baike.baidu.com/item'
        
        
    def search(self, str_item):
        url_search = self.url_base + '/' + str_item        
        self.driver.get(url_search)
        self.driver.implicitly_wait(2)
        page = self.driver.page_source
        return page    
    
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
            
        
 #%%       
#baike = Baike()
#content = baike.search_for_content('为爱放手')
