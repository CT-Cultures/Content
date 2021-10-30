# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 19:19:59 2021
CT-Cultures
@author: Herais
"""
#%% Import Global Libraries
import os
#import datetime

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

from bs4 import BeautifulSoup
#import lxml
import re
import pandas as pd
#%% Import Common Libraries
os.chdir('../Common')
from utils import DB
os.chdir('../imdb')
#%%
class QCC(DB):
    
    def __init__(self):
        
        super(QCC, self).__init__()
        
        # Define Relative Path        
        self.path_records = 'records'
        self.path_searches = 'searches'
        
        # Instantiate Selenium Driver
        self.mobile_emulation = { 
            "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" 
            }
        self.chromeoptions = webdriver.ChromeOptions()
        self.chromeoptions.add_argument('--headless')
        self.chromeoptions.add_argument('--no-sandbox')
        self.chromeoptions.add_argument('--disable-dev-shm-usage')
        self.chromeoptions.add_argument('--save-page-as-mhtml')
        #self.chromeoptions.add_experimental_option("mobileEmulation", self.mobile_emulation)
        self.driver = webdriver.Chrome(options = self.chromeoptions)
        self.url_base = 'https://www.qcc.com/'
        
        # Define Pages on IMDB
        self.landing_page = None
        self.most_popular_movies = None
        self.top_rated_movies = None

    def __version__(self):
        version = '1.0.0'
        self.__version__ = version
        print('Content-QCC-{}'.format(version))
        
    def get_landing_page(self):
        if not self.landing_page:
            self.driver.get(self.url_base)
            WebDriverWait(self.driver, 10)
            self.landing_page = self.driver.page_source
        return self.landing_page
    
    def search(self, key=None):
        url = self.url_base + '/web/search?key=' + key
        self.driver.get(url)
        WebDriverWait(self.driver, 10)
        element_npages = self.driver.find_element_by_class_name('fy_cur1')
        npages = element_npages.text
        
    