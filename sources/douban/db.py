# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 22:40:53 2021

@author: VXhpUS
"""
#%%
# Load Standard Library
import os
from urllib.request import Request, urlopen
import ssl

from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import 
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui

#%% setup search text
str_title = '我和我的祖国'
path_wip = 'wip'
path_save = path_wip + '/' + str_title + '.mhtml'

headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
url_base = 'https://search.douban.com/movie/subject_search?'
search_text = 'search_text={}'.format(str_title)
cat = '&cat=1002'
url_search = url_base + search_text + cat

path_wip = 'F:/Github/Content/sources/douban/wip'
#url_search = url_search.encode('ascii', 'ignore').decode('unicode_escape')

#%% Setup Chrome driver
chromeoptions = webdriver.ChromeOptions()
chromeoptions.add_argument('--headless')
chromeoptions.add_argument('--no-sandbox')
chromeoptions.add_argument('--disable-dev-shm-usage')
chromeoptions.add_argument('--save-page-as-mhtml')
#chromeoptions.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chromeoptions)

driver.get(url_search)
WebDriverWait(driver, 15)
#%%
# updated Nov 2019:
result = driver.find_element_by_id("suggResult")

print(result.text)
result.get_attribute('innerHTML')




#%%
actions = ActionChains(driver).key_down(Keys.CONTROL).send_keys('s').key_up(Keys.CONTROL)

actions.perform()
time.sleep(1)
pyautogui.press('enter')
#%%

# 1. 执行 Chome 开发工具命令，得到mhtml内容
time.sleep(1)
res = driver.execute_cdp_cmd('Page.captureSnapshot', {})

with open(path_save, 'w', newline='') as f: 
    f.write(res['data'])

f.close()