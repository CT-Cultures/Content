# -*- coding: utf-8 -*-
"""
Created on Thu May 27 11:53:28 2021

@author: VXhpUS
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 27 03:28:54 2021

@author: VXhpUS
"""


from Record_Registration import Registration
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
import random
import os
import pandas as pd

dy_reg = Registration()
#%%
links_of_registrations = dy_reg.links_of_registrations(links_of_publications, savefile=True)
#%%
contents = dy_reg.contents_of_registrations(links_of_registrations[0:3])
#%%
links_of_registrations = pd.read_csv('records/links_of_registrations.csv', encoding='utf-8-sig')
batch_size = 5
i = 14000
stop_i = 16000
fp = 'C://Users//Junting Liu//Documents//GitHub//Content//sources//ChinaFilm//records//contents_of_registrations_test14000_16000.csv'
while (i < stop_i):
    records = dy_reg.contents_of_registrations(links_of_registrations[i:i+batch_size])
    records.to_csv(fp, mode='a', header=(not os.path.exists(fp)), encoding='utf-8-sig', index=False)
    i += batch_size
    print(i, '-')
dy_reg.driver.close()
    #%%
from sys import platform
print(platform)