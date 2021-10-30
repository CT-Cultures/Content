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
    how='quick', save=True)
#%%

