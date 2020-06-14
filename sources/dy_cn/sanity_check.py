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
contents_of_registrations = 
contents_of_new_registrations = dy_reg.contents_of_new_registrations()


#%%
filename = "PubTheatricalRegistration_info_allregistrations"
if os.path.isfile(path_records + '//' + filename + '.csv'):
    records_existing = pd.read_csv(path_records + '//' + filename + '.csv', index_col=0, encoding='utf-8')
else:
    records_existing = pd.DataFrame(columns = ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接'])  
