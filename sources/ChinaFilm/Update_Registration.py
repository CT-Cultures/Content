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
contents_of_registrations_existing = dy_reg.contents_of_registrations_existing

#%%
links_of_new_publications = dy_reg.links_of_new_publications()
#%%
links_of_publications_exisiting_from_contents = contents_of_registrations_existing['公示批次链接'].unique()
