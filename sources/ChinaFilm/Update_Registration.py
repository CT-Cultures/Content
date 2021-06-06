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

# Update Registration Records
#contents_of_registrations = dy_reg.update_records(save_update=False)
contents_of_registrations = dy_reg.update_records(save_update=True)
#%%
links_of_new_registrations = dy_reg.links_of_new_registrations()
#%%
batch_size =5
i = 180
stop_i = links_of_new_registrations.shape[0]

fp = dy_reg.path_records + '/' + 'contents_of_registrations.csv'
while i < stop_i:
    records = dy_reg.contents_of_registrations(links_of_new_registrations[i:i+batch_size])
    records.to_csv(fp, mode='a', header=(not os.path.exists(fp)), encoding='utf-8-sig', index=False)
    i += batch_size
    print(i, '--------------------')
dy_reg.driver.close()
#%%
dy_reg.driver.close()
# Update and Save Release
#URS = MovieCN.UpdateRelease()
#links_of_newrelpub = URS.links_of_newpublications()
#contents_of_newrelpub = URS.contents_of_newpublications(savefile=True)