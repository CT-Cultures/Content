# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from dy_Registration import Registration
import pandas as pd
import numpy as np
import os

dy_reg = Registration()

#%%
links_of_pages = dy_reg.links_of_pages()
#%% links opublications
links_of_publications, links_of_publications_str = dy_reg.links_of_publications() # All Records
#links_of_new_publications = dy_reg.links_of_new_publications()
#links_of_new_publications = dy_reg.links_of_new_publications(update_records=True)
#%% links of registrations
links_of_registrations = dy_reg.links_of_registrations(links_of_publications, savefile=True)
#links_of_new_registrations = dy_reg.links_of_new_registrations()
#links_of_new_registrations = dy_reg.links_of_new_registrations(update_records=True)
#%% contents of registrations
#contents_of_registrations = dy_reg.contents_of_registrations(links_of_registrations) 
#contents_of_new_registrations = dy_reg.contents_of_new_registrations() 
contents_of_new_registrations = dy_reg.contents_of_new_registrations() 
 
#%%
links_of_publications['公示批次链接']
len(links_of_registrations['公示批次链接'].unique())

len(contents_of_new_registrations['公示批次链接'].unique().tolist())
#%%
path_records = 'records'
filename = "PubTheatricalRegistration_info_allregistrations"
path = path_records + '//' + filename + '.csv'

contents_of_registrations = pd.read_csv(path, encoding='utf-8')

links_of_publications.reset_index(inplace=True)
d = links_of_publications.to_dict(orient='dict')['公示批次链接']

contents_of_registrations['公示批次链接'] = contents_of_registrations['公示批次名称'].apply(lambda x: d[x] if x in d else np.nan)                                                         

    
    links_of_publications.loc[links_of_publications['名称'] == '国家电影局关于2020年01月下、02月全国电影剧本（梗概）备案、立项公示的通知', '公示批次链接'].tolist()[0]
links_of_publications.loc[66, '名称']


国家新闻出版广电总局电影局关于2017年12月（中旬）全国电影剧本（梗概）备案、...
