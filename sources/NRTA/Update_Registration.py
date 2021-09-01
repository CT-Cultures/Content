# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 13:10:15 2021

@author: VXhpUS
"""

from Record_Registration import Registration
import time

#%%
tv_reg = Registration()
#%%
links_of_pages = tv_reg.links_of_pages
#%%
links_of_publications = tv_reg.links_of_publications(savefile=True)
#%%
ls_reg_by_issue = []
#%%
for i, link in links_of_publications.iterrows():
    if 148 <= i < links_of_publications.shape[0]:
        print('----Acquiriing {}: {}----'.format(i, link['公示名称']))
        links_of_registrations = tv_reg.links_of_registrations(link.to_frame().T)
        contents_of_registrations = tv_reg.contents_of_registrations(links_of_registrations)
        print(','.join(contents_of_registrations['剧名'].tolist()), '。')
        ls_reg_by_issue.append(contents_of_registrations)
        time.sleep(5)
#%%
import pandas as pd
contents_of_registrations = pd.concat([ls_reg_by_issue[i] for  i in range(len(ls_reg_by_issue))], ignore_index=True)
#%%
contents_of_registrations.to_json(tv_reg.save_records(contents_of_registrations, 'contents_of_registrations'))
#%%