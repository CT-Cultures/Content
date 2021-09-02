# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 13:10:15 2021

@author: VXhpUS
"""

from Record_Registration import Registration
import time
import os
import pandas as pd

#%%
tv_reg = Registration()

#%%
path_records = 'records'    
fn_links_of_publications = "links_of_publications"
fn_contents_of_registrations = "contents_of_registrations"
fn_links_of_registrations = 'links_of_registrations'
#%%

contents_of_registrations_existing = tv_reg.contents_of_regstrations_existing
links_of_registrations_existing = tv_reg.links_of_registrations_existing
links_of_publications_existing = tv_reg.links_of_publications_existing

#%%
links_of_registrations_latest = tv_reg.links_of_registrations(links_of_publications_existing)