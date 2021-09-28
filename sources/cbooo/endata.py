# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 21:36:16 2021

@author: VXhpUS
"""


from urllib.request import Request, urlopen
from urllib.error import HTTPError
import ssl

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import re
import time
#%%
class endata(object):
    
    def __init__(self):
        if not self:
            raise ValueError
        self.path_records = 'wip'
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}

        self.chromeoptions = webdriver.ChromeOptions()
        self.chromeoptions.add_argument('--headless')
        self.chromeoptions.add_argument('--no-sandbox')
        self.chromeoptions.add_argument('--disable-dev-shm-usage')
        self.chromeoptions.add_argument('--save-page-as-mhtml')
        self.driver = webdriver.Chrome(options = self.chromeoptions)
        self.url_base = 'https://www.endata.com.cn/BoxOffice/search.html?key='
            
    def search(self, str_item) -> str:
        str_item = str_item
        url_search = self.url_base + '/' + str_item
        self.driver.get(url_search)
        wait = WebDriverWait(self.driver, 60)

        posts_xpath = '//div[@class="box-office-wrap"]/div]'
        wait.until(EC.presence_of_element_located((By.XPATH, posts_xpath)))
        #page = self.driver.page_source
        ret = self.driver.find_element_by_class_name('search-item')
        ret1 = self.driver.execute_script('return document.body.innerHTML')
        #ret1 = ret.text
        return ret1
    
    
    def search_urlopen(self, str_item) ->str:
        str_item  = str_item.encode('ascii', 'ignore').decode('unicode_escape')
        req = Request(url=self.url_base + '/' + str_item, 
                      headers=self.headers
                     )
        # ctx for expired ssl certificate
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE    
        with urlopen(req, context=ctx) as x: 
            html = x.read().decode('utf-8')
        return html