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

#%%
class Baike(object):

    def __init__(self):
        if not self:
            raise ValueError
    
    def search_for_content(self, str_item):
        url_search = 'https://baike.baidu.com/item/' + str_item        
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        driver.get(url_search)
        driver.implicitly_wait(2)
        page = driver.page_source
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
    
    def batchsearch_for_content(self, list_str_items):
        list_title_content = []
        for item in list_str_items:
            content = self.search_for_content(item)
            list_title_content = [item, content]
        return list_title_content
            
        
 #%%       
#baike = Baike()
#content = baike.search_for_content('为爱放手')
