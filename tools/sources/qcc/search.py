# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 00:48:56 2021

@author: VXhpUS
"""

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

#%%
from QCC import QCC
qcc = QCC()

#%%

def search(key=None):
    url_base = 'https://www.qcc.com/'
    url = url_base + '/web/search?key=' + key
    qcc.driver.get(url)
    WebDriverWait(qcc.driver, 10)
    element_npages = qcc.driver.find_element_by_class_name('fy_cur1')
    npages = element_npages.text
    
#%%
key= '北京中视皮皮影业有限公司'
url_base = 'https://www.qcc.com/'
url = url_base + '/web/search?key=' + key

qcc.driver.get(url_base)
WebDriverWait(qcc.driver, 10)

#%%
#<form action="/search" class="search-form" id="indexSearchForm"> 
#<div class="input-group"> 
#<input type="text" id="searchkey" maxlength="1000" autocomplete="off" placeholder="请输入企业名、人名、产品名、或地址电话/经营范围等，多关键词用空格隔开，如“苏州 企查查”" name="key" class="form-control index-searchkey active" required="required"> 
#<input type="hidden" id="index" name="index" value="0"> <span class="input-group-btn"> 
#<input type="submit" class="index-searchbtn" value="查一下" required="required"> </span> 
#</div> <a data-trigger="hover" data-tooltip="arrow" data-toggle="tooltip" data-placement="bottom" title="" onclick="showBatchSearchModal();zhugeTrack('主页搜索框区域点击',{'内容类型':'批量查询'});" class="ibatch-btn" data-original-title="批量查询"></a> 
#<div class="oversea-select" id="overseaSelect" onclick="dropDownOverseaCountry()"> <span>全球</span> <b class="caret"></b> <input type="hidden" name="overseacountry" value=""> </div> <a rel="nofollow" onclick="zhugeTrack('主页搜索框区域点击',{'高级查询':'高级查询'});loginPermision(event)" class="adsearch-btn" href="/user_login?back=/search_adsearchmulti">高级<br>查询</a> </form>
element_form = qcc.driver.find_element(By.XPATH, "//form[@id='indexSearchForm']")
element_search = element_form.find_element(By.XPATH, "//input[@id='searchkey']")

#element_search.click()
#%%

element_search.sendKeys(key)


#%%
ActionChains(qcc.driver).move_to_element(element_search
    ).click().send_keys_to_element(element_search, key).perform()

#%%
element_button = element_form.find_element(By.XPATH, "//input[@type='submit']")
ActionChains(qcc.driver).move_to_element(element_button
    ).click().perform()

#%%
elements_table = qcc.driver.find_elements(By.TAG_NAME, 'table')

#%%
elements_tr =  elements_table[0].find_elements(By.TAG_NAME, "tr")

#%%
elements_td  = elements_tr[1].find_elements(By.TAG_NAME, "td")

#%%
for element in elements_td:
    print(element.)

#%%
elements_a[0].get_attribute('name')
