from Record_Registration import Registration
from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
import random

dy_reg = Registration()
#%%
links_of_registrations = dy_reg.links_of_registrations(links_of_publications, savefile=True)
#%%
contents = dy_reg.contents_of_registrations(links_of_registrations[0:3])
#%%
batch_size = 50
i = 0
while i < len(links_of_registrations):
    records = dy_reg.contents_of_registrations(links_of_registrations[i:i+batch_size])
    records.to_csv('/records/contents_of_registrations.csv', mode='a',encoding='utf-8-sig', index=False)
    i += batch_size
    print(i)