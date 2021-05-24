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
batch_size = 25
i = 300
fp = 'D://Github//Content//sources//ChinaFilm//records//contents_of_registrations_test.csv'
while i < len(links_of_registrations):
    records = dy_reg.contents_of_registrations(links_of_registrations[i:i+batch_size])
    records.to_csv(fp, mode='a', header=(not os.path.exists(fp)), encoding='utf-8-sig', index=False)
    i += batch_size
    print(i, '-')
dy_reg.driver.close()
    #%%
from sys import platform
print(platform)