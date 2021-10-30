# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 02:21:37 2021

@author: VXhpUS
"""
#%%
# Load Standard Library
# Load Standard Library
import os
#from sys import platform
from urllib.request import Request, urlopen
import ssl
#from urllib.error import HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import datetime
from datetime import date
from datetime import timedelta
import time

# Load from Local
#from IO_Storage import File

######################################################################
class Reg_Modifications(object):
    
    def __init__(self):
        
        super(Reg_Modifications, self).__init__()
        
        # 中国电影电子政务平台网址
        self.url_base = "https://dsj.nrta.gov.cn"
        
        # 电影电子政务平台备案公示网址
        self.url_registration = "https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=changing&pageIndex=1"
        
        # url_browser head
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # folder for aving logs, relative
        self.path_logs = 'logs'    
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()
        
        # read existing contents of registrations
        self.contents_of_regmod_existing = pd.DataFrame()
        if os.path.isfile(self.path_records + '//'  + 'contents_of_reg_modification.json'):
            self.contents_of_reg_modification_existing  = pd.read_json(
                self.path_records + '//'  + 'contents_of_reg_modification_existing .json')
                  
        # read existing links of publications
        self.links_of_regmod_publications_existing = pd.DataFrame()
        if os.path.isfile(self.path_records + '//'  
            + 'links_of_regmod_publications.json'):
                self.links_of_publications_existing = pd.read_json(
                    self.path_records + '//'  + 'links_of_regmod_publications')  