# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 15:55:01 2019

@author: VX
"""
#%% Import Standard Library
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import time
import requests
import json
from pathlib import Path
import random
import datetime

#%% Import Custom Library
import MovieCN

#%%
class Mtime(object):
    url_basesite = "http://www.mtime.com/"
    url_recordpage = "http://movie.mtime.com/"
    prefix_query = "?q="
   
    def __init__(self):
        if not self:
            raise ValueError         
# =============================================================================
    def all_searchid(self):
        url_landingpage = 'http://movie.mtime.com/movie/search/section/'
        with urlopen(url_landingpage) as x: 
            html = x.read().decode('utf-8')
        pattern_split = re.compile(r'<strong>.*?</strong>.*?<dd class="clearfix"')
        pattern_name_category = re.compile(r'<strong>.*?</strong>')
        html_categories = pattern_split.findall(html)
        search_values = ()
        for item in html_categories:
#            print(item)
            name_category = pattern_name_category.search(item).group().lstrip('<strong>').rstrip('：</strong>')
#            print(name_category)
            bsObj = BeautifulSoup(item, 'html5lib')
            for value in bsObj.find_all('a', cvalue=True):
                c_value = value.get("cvalue")
                description = value.get_text()
                search_values += ([name_category, c_value, description],)                 
# 补上年代
        pattern_year = re.compile(r'<strong>年代.*?<strong>')
        html_year = pattern_year.search(html).group()
#        print(html_year)
        bsObj = BeautifulSoup(html_year, 'html5lib')
        name_category = bsObj.strong.get_text().strip('：')
#        print(name_category)
        list_year = bsObj.find_all('li')
        for each in list_year:
            year_range = each.get_text().lstrip().rstrip()
            search_values += ([name_category,'NA', year_range],)
#            print(year_range)
# 补上色彩
        pattern_color = re.compile(r'<strong>色彩.*?</div>')
        html_color = pattern_color.search(html).group()
        #        print(html_color)
        bsObj = BeautifulSoup(html_color,'html5lib')
        name_category = bsObj.strong.get_text().strip('：')
        #        print(name_category)
        list_color = bsObj.find_all('li')
        for each in list_color:
            c_value = each.a.get("cvalue")
            color = each.get_text().lstrip().rstrip()
            search_values += ([name_category, c_value, color],)
        return search_values
# =============================================================================         
    def geturl_search(self, pagenumber):
        t = time.strftime('%Y%m%d%H%M%S0000',time.localtime())
        url_ajax =r'http://service.channel.mtime.com/service/search.mcs'\
                   r'?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService'\
                   r'&Ajax_CallBackMethod=SearchMovieByCategory'\
                   r'&Ajax_CrossDomain=1'\
                   r'&Ajax_RequestUrl='\
                   r'http%3A%2F%2Fmovie.mtime.com%2Fmovie%2Fsearch%2Fsection%2F%23nation%3D138%26sortType%3D4%26viewType%3D1'\
                   r'&t={t}'\
                   r'&Ajax_CallBackArgument0='\
                   r'&Ajax_CallBackArgument1=0'\
                   r'&Ajax_CallBackArgument2={id_region}'\
                   r'&Ajax_CallBackArgument3=0'\
                   r'&Ajax_CallBackArgument4=0'\
                   r'&Ajax_CallBackArgument5=0'\
                   r'&Ajax_CallBackArgument6=0'\
                   r'&Ajax_CallBackArgument7=0'\
                   r'&Ajax_CallBackArgument8='\
                   r'&Ajax_CallBackArgument9=0'\
                   r'&Ajax_CallBackArgument10=0'\
                   r'&Ajax_CallBackArgument11=0'\
                   r'&Ajax_CallBackArgument12=0'\
                   r'&Ajax_CallBackArgument13=0'\
                   r'&Ajax_CallBackArgument14=1'\
                   r'&Ajax_CallBackArgument15=0'\
                   r'&Ajax_CallBackArgument16=1'\
                   r'&Ajax_CallBackArgument17=4'\
                   r'&Ajax_CallBackArgument18={pagenumber}'\
                   r'&Ajax_CallBackArgument19=1'.format(id_region=str(138),t=t,pagenumber=pagenumber)
        return url_ajax
    
    # Argument2: {region}
    # Argument3: {类型号}
    # Argument9：{Year年代}
    # Argument10:{Year年代}
    # Argument14:{中文拼音首字母， ie'J',不填=1}
    # Argument16：{英文首字母，不填=1}
    # Argument18:{pagenumber}
    # Argument19：{0=gridview,1=listview}
# =============================================================================
    
    def getpage_ifvalid(self, url):
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        driver.get(url)
        driver.implicitly_wait(5)
        page = driver.page_source
        pattern_valid = re.compile(r'"vcodeValid":true')
        pattern_notvalid = re.compile(r'"vcodeValid":false')
        if pattern_valid.search(page):
            return page
        elif pattern_notvalid.search(page):
            return None

# 抓取中国电影的 影片链接        
    def get_links_movies_CN(self,num_startpage,num_endpage):
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        i = num_startpage
        list_of_pageSource = []
        while i < (num_endpage+1):
            url_ajax = self.geturl_search(i)
            test = self.getpage_ifvalid(url_ajax)
#            print(test)
            if test == None:
                print("server returns robot, link at: " + url_ajax)
                break
#                time.sleep(30)
#                i = i+0
            else:
                print("add page true, page number: " + str(i))
                list_of_pageSource = list_of_pageSource + [test]
                i = i + 1
                time.sleep(2)
#            driver.get(url_ajax)
        return list_of_pageSource
        driver.close()
        
    def get_movielinks_singlepage(self,text):
#        json_pattern = re.compile(r'=(.*?);')
#        result=json_pattern.findall(text)[0]
        pattern = re.compile(r'h3 class=.*?;/h3')
        movies = pattern.findall(text)
#        print(movies)
        titles = []
        for item in movies:
            pattern_name_cn = re.compile(r'_blank.*?&amp')
            name_cn = pattern_name_cn.search(item).group().lstrip('_blank\\"&gt;').rstrip('&amp')
            pattern_id = re.compile(r'http://movie.mtime.com/.*?/')
            id_movie = pattern_id.search(item).group().lstrip('http://movie.mtime.com/').rstrip('/') # 改成findall more than 1
            titles.append([name_cn, id_movie])
#            print(titles)
        return titles

    def get_movielinks(self, list_of_pages):
        links_movies= []
        for page in list_of_pages:
            list_titles = self.get_movielinks_singlepage(page)
            links_movies = links_movies + list_titles
        return links_movies
# =============================================================================    