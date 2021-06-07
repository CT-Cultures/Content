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
#contents_of_registrations = dy_reg.update_records(i==[pickup_index],batch_size=5)
#%%
dy_reg.save_records(contents_of_registrations, 'contents_of_registrations', backup=True)
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