# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 12:40:28 2021

@author: VXhpUS
"""

#%% Import Libraries, Instantiate Classes

#from bs4 import BeautifulSoup
#import pandas as pd
#import re

from zgdypw import ZGDYPW
zgd = ZGDYPW()

#%% Update Contents of Releases
contents_of_releases = zgd.update_contents_of_releases(
    how='comprehensive', save=True)
#%%

links_of_marketpage_latest = zgd.links_of_marketpage()
links_of_releases_latest = zgd.links_of_releases(
    links_of_marketpage_latest) # List[str]

df_links_of_releases_latest = \
    pd.Series(links_of_releases_latest).rename('publink').to_frame()

contents_of_releases_existing = pd.read_json(
    zgd.path_records + '/' + "contents_of_releases" + '.json')

publications_unique = \
    contents_of_releases_existing['publink'].unique()
    
links_of_publications_new = df_links_of_releases_latest[
    ~df_links_of_releases_latest['publink'].isin(publications_unique)
]

links_of_releases_new = zgd.links_of_releases(
    links_of_publications_new['publink'].tolist())
