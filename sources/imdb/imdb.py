# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 02:53:16 2021
Content
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

class IMDB(DB):
    
    def __init__(self):
        
        super(IMDB, self).__init__()
        
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
        self.url_base = 'https://www.imdb.com'
        
        # Define Pages on IMDB
        self.landing_page = None
        self.most_popular_movies = None
        self.top_rated_movies = None
        
    
    def __version__(self):
        version = '1.0.0'
        self.__version__ = version
        print('Content-IMDB-{}'.format(version))
    
    def get_landing_page(self):
        if not self.landing_page:
            self.driver.get(self.url_base)
            WebDriverWait(self.driver, 10)
            self.landing_page = self.driver.page_source
        return self.landing_page
    
    def get_most_popular_movies(self):
            
        if self.most_popular_movies == None:
            if self.landing_page == None:
                self.landing_page = self.get_landing_page()
            
            # Navigate to Menu and Click
            element_menu = self.driver.find_element_by_id(
                "imdbHeader-navDrawerOpen")
            ActionChains(self.driver).move_to_element(
                element_menu).click(element_menu).perform()
            
            # Navigate to Movie Category and Click
            element_movie = element_menu.find_element(
                By.XPATH, "//label[@for='nav-link-categories-mov']")
            ActionChains(self.driver).move_to_element(
                element_movie).click(element_movie).perform()
            
            # Navigate to Most Popuplar Movies and Click
            element_mpm = element_movie.find_element(
                By.XPATH, "//a[@href='/chart/moviemeter/?ref_=nv_mv_mpm']")
            ActionChains(self.driver).move_to_element(
                element_mpm).click(element_mpm).perform()
            WebDriverWait(self.driver, 10)
            
            html = self.driver.page_source
            self.most_popular_movies = IMDB.dfparse_table_movies(html)
            
            DB.save_search(self.most_popular_movies, suffix='mpm')
        
        return self.most_popular_movies
    
        
    def get_top_rated_movies(self):
            
        if self.top_rated_movies == None:
            if self.landing_page == None:
                self.landing_page = self.get_landing_page()
            
            # Navigate to Menu and Click
            element_menu = self.driver.find_element_by_id(
                "imdbHeader-navDrawerOpen")
            ActionChains(self.driver).move_to_element(
                element_menu).click(element_menu).perform()
            
            # Navigate to Movie Category and Click
            element_movie = element_menu.find_element(
                By.XPATH, "//label[@for='nav-link-categories-mov']")
            ActionChains(self.driver).move_to_element(
                element_movie).click(element_movie).perform()
            
            # Navigate to Most Popuplar Movies and Click
            element_trm = element_movie.find_element(
                By.XPATH, "//a[@href='/chart/top/?ref_=nv_mv_250']")
            ActionChains(self.driver).move_to_element(
                element_trm).click(element_trm).perform()
            WebDriverWait(self.driver, 10)
            
            html = self.driver.page_source
            self.top_rated_movies  = IMDB.dfparse_table_movies(html)
            
            DB.save_search(self.top_rated_movies, suffix='trm')
        
        return self.top_rated_movies
    
    @staticmethod
    def dfparse_table_movies(html:str) -> pd.DataFrame:
        """
        This functions parses most_popular_movies in html str format
        to pd.DataFrame

        Parameters
        ----------
        html : str
            DESCRIPTION.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        soup = BeautifulSoup(html, 'lxml')
        table = soup.table
        ls = []
        trs =  table.find_all('tr')
        for tr in trs[1:]:
            d = {}
            tds = tr.find_all('td')
            d['rk'] = tds[0].find('span', {'name':'rk'})['data-value']
            d['ir'] = tds[0].find('span', {'name':'ir'})['data-value']
            d['fid'] = tds[0].find('a')['href'].split('/')[2]
            d['title'] = tds[0].find('img')['alt']
            d['img'] = tds[0].find('img')['src']
            d['creatives'] = tds[1].find('a')['title'].split(',')
            d['year'] = tds[1].find(
                'span', class_='secondaryInfo').text.strip('(').rstrip(')')
            if tds[2].find('strong'):
                d['nvotes'] = tds[2].find('strong')['title'].split(' ')[3]
            ls.append(d)
        df = pd.DataFrame.from_dict(ls)
        return df