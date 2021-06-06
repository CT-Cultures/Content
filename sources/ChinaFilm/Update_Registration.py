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

#%%
contents_of_registrations = dy_reg.update_records(batch_size=5)
#%%
links_of_new_publications = dy_reg.links_of_new_publications(update_records=True)
#%%
links_of_new_registrations = dy_reg.links_of_new_registrations(update_records=True)
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

def content_of_registrations_in_batch(self, 
                                    links_of_registrations: pd.DataFrame, 
                                    filename: str = "contents_of_registrations",
                                    i: int = 0,
                                    batch_size: int = 5,
                                    savefile: bool = False
                                    )
    while i < links_of_registrations.shape[0]:
        records = self.contents_of_registratons(links_of_registrations[i:i+batch_size])
        i += batch_size
        print(i, '--------------------')
        if i == 100 or i == records.shape[0]-1: self.append_records(records, filename, backup=True)
        else: self.append_records(records, filename, backup=False)
        return i 
#%%
dy_reg.driver.close()
# Update and Save Release
#URS = MovieCN.UpdateRelease()
#links_of_newrelpub = URS.links_of_newpublications()
#contents_of_newrelpub = URS.contents_of_newpublications(savefile=True)