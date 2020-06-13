# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from MovieCN import GetRegistration

import pandas as pd
#%%
GR = GetRegistration()
#links_allpages = GR.links_of_pages()

links_of_publications = GR.links_of_publications(savefile=True)

#test = pd.DataFrame(links_of_publications)
#test.columns = ['公示批次链接','名称']