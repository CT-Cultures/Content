# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 13:10:15 2021

@author: VXhpUS
"""
#%% import libraries
from Record_Registration import Registration

#%% instantiate tv_reg
tv_reg = Registration()

#%% update and save
tv_reg.update_records(how='quick', save_update=True)

#%%
import pandas as pd

reg = pd.read_json('records/contents_of_registrations.json', orient='split')