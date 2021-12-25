# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 10:06:27 2021
ContentAI
@author: Herais
"""
#%% Import Libraries
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.command import Command
#%% instantiate imdb
from imdb import IMDB
imdb = IMDB()
#%%
df_mpm = imdb.get_most_popular_movies()

#%%
element_table = imdb.driver.find_element(By.XPATH, "//table")
#%%
elements_td = element_table.find_elements(By.CLASS_NAME, "posterColumn")
#%%

html = imdb.driver.page_source
#%%

#%% Get movie pages from table
path_wip = 'wip'
element_table = imdb.driver.find_element(By.XPATH, "//table")
elements_td = element_table.find_elements(By.CLASS_NAME, "posterColumn")
i = 0
L = len(elements_td)
while i < L:
    element_a = elements_td[i].find_element(By.XPATH, "a")
    fid = element_a.get_attribute('href').split('/')[4] #str
    ActionChains(imdb.driver).move_to_element(
        element_a).click(element_a).perform()
    WebDriverWait(imdb.driver, 12)
    html =  imdb.driver.page_source
    fn = 'wip/{}_mpm.html'.format(fid)
    with open(fn, 'w') as f:
        f.write(html)
    f.close()
    imdb.driver.back()
    WebDriverWait(imdb.driver, 3)
    element_table = imdb.driver.find_element(By.XPATH, "//table")
    elements_td = element_table.find_elements(By.CLASS_NAME, "posterColumn")
    i += 1
    