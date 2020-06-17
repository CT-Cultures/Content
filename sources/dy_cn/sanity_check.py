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
 
#%%
links_of_publications = pd.read_csv('records//links_of_publications.csv', encoding='utf-8-sig')
links_of_registrations = pd.read_csv('records//links_of_registrations.csv', encoding='utf-8-sig')
contents_of_registrations = pd.read_csv('records//contents_of_registrations.csv', encoding='utf-8-sig')
#%%
fn_links_of_publications = "links_of_publications"
fn_links_of_registrations = "links_of_registrations" 
fn_contents_of_registrations = "contents_of_registrations"
path_records = 'records'

path_records + '//' + fn_links_of_publications + '.csv'

if os.path.isfile(path_records + '//' + fn_links_of_publications + '.csv'):
    links_of_publications = pd.read_csv(path_records + '//' + fn_links_of_publications + '.csv', encoding='utf-8-sig')
else:
    links_of_publications = links_of_publications('empty')

if os.path.isfile(path_records + '//' + fn_links_of_registrations + '.csv'):
    links_of_registrations = pd.read_csv(path_records + '//' + fn_links_of_registrations + '.csv', encoding='utf-8-sig')
else:
    links_of_registrations = links_of_registrations(links_of_publications=pd.DataFrame())
    
if os.path.isfile(path_records + '//' + fn_contents_of_registrations + '.csv'):
    contents_of_registrations = pd.read_csv(path_records + '//' + fn_contents_of_registrations + '.csv', encoding='utf-8-sig')
else:
    contents_of_registrations = contents_of_registrations(links_of_registrations = pd.DataFrame())

links_of_publications_latest = dy_reg.links_of_publications()
# save
dy_reg.save_records(links_of_publications_latest, 'links_of_publications')
            
#%%
lp_latestest_not_in_lp_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(links_of_publications['公示批次链接'])]
lp_old_not_in_lp_latest = links_of_publications[~links_of_publications['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]

lp_latest_not_in_lr_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(links_of_registrations['公示批次链接'])]
lr_old_not_in_lp_latest = links_of_registrations[~links_of_registrations['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]

lp_latest_not_in_cr_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(contents_of_registrations['公示批次链接'])]
cr_old_not_in_lp_latest = contents_of_registrations[~contents_of_registrations['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]

lr_old_not_in_cr_old = links_of_registrations[~links_of_registrations['制作表链接'].isin(contents_of_registrations['制作表链接'])]
cr_old_not_in_lr_old = contents_of_registrations[~contents_of_registrations['制作表链接'].isin(links_of_registrations['制作表链接'])]

links_of_publications_to_update = pd.concat([   lp_latestest_not_in_lp_old['公示批次链接'],
                                                lp_old_not_in_lp_latest['公示批次链接'],
                                                lp_latest_not_in_lr_old['公示批次链接'],
                                                lr_old_not_in_lp_latest['公示批次链接'],
                                                lp_latest_not_in_cr_old['公示批次链接'],
                                                cr_old_not_in_lp_latest['公示批次链接'],
                                                lr_old_not_in_cr_old['公示批次链接'],
                                                cr_old_not_in_lr_old['公示批次链接']
                                            ], axis=0, ignore_index=True)

links_of_publications_to_update.drop_duplicates(inplace=True)
links_of_publications_to_update = links_of_publications_to_update.reset_index()

links_of_registrations_to_update = dy_reg.links_of_registrations(links_of_publications_to_update)
links_of_registrations_updated = pd.concat([links_of_registrations,
                                            links_of_registrations_to_update],
                                           axis=0, ignore_index=True)
links_of_registrations_updated.drop_duplicates(subset='制作表链接', inplace=True)
links_of_registrations_updated.reset_index(drop=True)
dy_reg.save_records(links_of_registrations_updated, 'links_of_registrations')

contents_of_registrations_to_update = dy_reg.contents_of_registrations(links_of_registrations_to_update)
contents_of_registrations_updated = pd.concat([contents_of_registrations,
                                               contents_of_registrations_to_update],
                                              axis=0, ignore_index=True)
contents_of_registrations_updated.drop_duplicates(subset='制作表链接', inplace=True)
contents_of_registrations_updated.reset_index(drop=True, inplace=True)
dy_reg.save_files(contents_of_registrations_updated, 'contents_of_registrations')

check = contents_of_registrations_updated[~contents_of_registrations_updated['制作表链接'].isin(links_of_registrations_updated['制作表链接'])]
links_of_registrations_updated['制作表链接'].isin(contents_of_registrations_updated['制作表链接'])

cr_duplicated = contents_of_registrations_updated[contents_of_registrations_updated['制作表链接'].duplicated(keep=False)]
#%%

links_of_publications_to_update = pd.DataFrame()

len_lp = links_of_publications['公示批次链接'].shape[0]
len_lr = links_of_registrations['公示批次链接'].shape[0]
len_lr_unique = links_of_registrations['公示批次链接'].drop_duplicates().shape[0]

len_lr_prod = links_of_registrations['制作表链接'].shape[0]
len_cr_prod = contents_of_registrations['制作表链接'].shape[0]

len_cr = contents_of_registrations['公示批次链接'].shape[0]

#if len_lp > len_lr_unique:
 
t = pd.concat([contents_of_registrations['制作表链接'], links_of_registrations['制作表链接']], axis=0, ignore_index=True)
t.drop_duplicates(inplace=True)

#%%
t = links_of_registrations.loc[~links_of_registrations['制作表链接'].isin(contents_of_registrations['制作表链接']), '公示批次链接']
t.drop_duplicates(inplace=True)
