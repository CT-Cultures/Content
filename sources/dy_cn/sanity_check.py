# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from dy_Registration import Registration
import pandas as pd
import re


import numpy as np
import os
from datetime import date

dy_reg = Registration()

#%%
links_of_pages = dy_reg.links_of_pages
#%% links opublications
links_of_publications = dy_reg.links_of_publications(savefile=True) # All Records
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

#%% update_records

up_to_date_records_raw = dy_reg.update_records(save_update=False)

#%%
contents_of_registrations_raw = pd.read_csv('records/contents_of_registrations.csv', encoding='utf-8-sig')

#%%\
contents_of_registrations_raw['公示日期'].agg(dy_reg.parser.PubDate)
contents_of_registrations_raw['公示日期']

#%%
contents_of_registrations_raw['公示批次名称'].agg(dy_reg.parser.PubTitle)
contents_of_registrations['公示批次名称'] 

contents_of_registrations.columns

#%%
contents_of_registrations_raw['备案立项号'].agg(dy_reg.parser.RegType)

contents_of_registrations_raw[contents_of_registrations_raw['备案立项号'].isna()]
#%%
contents_of_registrations_refined = dy_reg.Refined_Records(update_first=False)
#%%
contents_of_registrations_raw['备案立项号'].agg(dy_reg.parser.RegSequenceNo)
#%%
contents_of_registrations_raw.columns
def pubtitle(pubtitle):
        
    pat = re.compile(u'关于.*全国')
    pt = pat.search(pubtitle)
    if pt:
        pt = pt.group()
        pt = pt.lstrip('关于').rstrip('全国')
    else:
        pt = np.nan
    #2016年09月（下旬）10月（上旬）
    #2020年01月下、02月
    #2019年08月（上旬）
    #2017年09月（下旬）、10月（上旬）
    #2017年09月（中旬）
    #2015年09月（下旬）、10月（上旬）
    #2013年04月（下旬）、05月（上旬）
    #2012年01月
    #2011年12月（下旬）   
    if pt:
        yr, r = pt.split('年')[0], pt.split('年')[1]
        ms = re.split('[）\)]', r)
        if len(ms) == 1:
            start_m = 
    
    return start_m
        

pubtitle('国家电影局关于2020年01月下、02月全国电影剧本（梗概）备案、立项公示的通知')

t = '09月（下旬）10月（上旬）'
t2 ='2012年01月'
test =re.split('[）\)]', t)



test = contents_of_registrations_raw['公示批次名称'].agg(pubtitle)  


def issue_daterange(pubtitle: pd.Series):
    pubtitle_unique = pubtitle.drop_duplicates()
    pubtitle_unique_prev = pubtitle_unique.shift(-1).rename('上一期公示批次名称')
    pubtitle_curr_prev = pd.concat([pubtitle_unique, pubtitle_unique_prev], axis=1)

pubtitle_unique = contents_of_registrations_refined['公示批次名称'].drop_duplicates()
pubtitle_unique_prev = pubtitle_unique.shift(-1).rename('上一期公示批次名称')
pubtitle_curr_prev = pd.concat([pubtitle_unique, pubtitle_unique_prev], axis=1)









