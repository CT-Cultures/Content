# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from dy_Registration import Registration
import pandas as pd
import os

dy_reg = Registration()

#%% links of pages and publications
links_of_pages = dy_reg.links_of_pages()
links_of_publications = dy_reg.links_of_publications() # All Records
links_of_new_publications = dy_reg.links_of_new_publications()
#links_of_new_publications = dy_reg.links_of_new_publications(update_records=True)
#%% links of registrations
#links_of_registrations = dy_reg.links_of_registrations(links_of_publications)
links_of_new_registrations = dy_reg.links_of_new_registrations()
#links_of_new_registrations = dy_reg.links_of_new_registrations(update_records=True)
#%% contents of registrations
#contents_of_registrations = dy_reg.contents_of_registrations(links_of_registrations) 
contents_of_new_registrations = dy_reg.contents_of_new_registrations(update_records=True) 
 

#%%
path_records = 'records'
filename = "PubTheatricalRegistration_info_allregistrations"
path = path_records + '//' + filename + '.csv'

os.path.isfile(path)
os.path.isfile(path_records + '//' + filename + '.csv')
