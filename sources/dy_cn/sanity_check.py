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

up_to_date_records_raw = dy_reg.update_records(save_update=True)

#%%
contents_of_registrations_raw = pd.read_csv('records/contents_of_registrations.csv', encoding='utf-8-sig')
#%%\
contents_of_registrations_raw['公示日期'].agg(dy_reg.parser.PubDate)
contents_of_registrations_raw['公示日期']

#%%
contents_of_registrations_raw

contents_of_registrations['公示批次名称'] = contents_of_registrations_raw.agg(dy_reg.parser.correct_publication_title_errors, axis=1)
contents_of_registrations 