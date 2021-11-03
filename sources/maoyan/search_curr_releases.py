# -*- coding: utf-8 -*-
"""
Content
Created on Mon Sep 27 13:55:23 2021
@author: Herais
"""
#%% Load Global Libraries
#%% Load Local Libraries
from maoyan import MAOYAN
my = MAOYAN()
#%%
df_ret = my.on_screen()

#%%


url = 'https://maoyan.com/films?showType=2'
page = my.get_page_source(url)

#%%
from bs4 import BeautifulSoup

soup = BeautifulSoup(page)

mpanel = soup.body.find('div', class_='movies-panel')

#%%
import re
links_page = []
for link in mpanel.find_all('a', class_=re.compile('page_')):
    if link['href'] == "javascript:void(0);":
        links_page.append(url)
    else:
        links_page.append(url + link['href'])

links_page = list(set(links_page))
#%%
url_search = 'https://maoyan.com/query?kw=' + '乌海'
res = my.search_for_score(url_search)