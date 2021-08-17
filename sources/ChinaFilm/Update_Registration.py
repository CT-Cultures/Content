# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 23:32:35 2019

@author: VSurfacePro3
"""
#%%
import os
import pandas as pd
from Record_Registration import Registration

dy_reg = Registration()
#%%
df = dy_reg.Refined_Records(update_first =True)
#%
#%%
dy_reg.save_records(contents_of_registrations, 'contents_of_registrations')
#%%
contents_of_registrations_existing = pd.read_csv('records/contents_of_registrations.csv').reset_index(drop=True)
#%%
contents_of_registrations = contents_of_registrations_existing.sort_values('公示日期', ascending=False)
#%%
# Update Registration Records
#contents_of_registrations = dy_reg.update_records(save_update=False)
contents_of_registrations_new = pd.read_csv('contents_of_registrations_in_batch.csv')
contents_of_registrations_existing = pd.read_csv('contents_of_registrations.csv')
###
contents_of_reg = pd.concat([contents_of_registrations_new, contents_of_registrations_existing], ignore_index=True)
###
#%%
contents_of_reg = contents_of_reg.drop_duplicates()
#%%
contents_of_registrations = dy_reg.update_records(batch_size=0)
#contents_of_registrations = dy_reg.update_records(i==[pickup_index],batch_size=5)
#%%
dy_reg.save_records(contents_of_reg, 'contents_of_registrations', backup=True)
#%%
links_of_new_publications = dy_reg.links_of_new_publications(update_records=True)
#%%
links_of_new_registrations = dy_reg.links_of_new_registrations(update_records=True)
#%%
dy_reg.driver.close()
# Update and Save Release
#URS = MovieCN.UpdateRelease()
#links_of_newrelpub = URS.links_of_newpublications()
#contents_of_newrelpub = URS.contents_of_newpublications(savefile=True)