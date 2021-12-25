<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 21:19:01 2021

@author: VXhpUS
"""
from bs4 import BeautifulSoup
from Baike import Baike
import pandas as pd

#%%
baike = Baike()

#%%
str_item = '关于我妈的一切'
res = baike.search(str_item)
res1 = baike.search_for_content(str_item)

#%%
baike.get_talents(res)
#%%
=======
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 21:19:01 2021

@author: VXhpUS
"""
from bs4 import BeautifulSoup
from Baike import Baike
import pandas as pd

#%%
baike = Baike()

#%%
str_item = '只要你过得比我好'
res = baike.search(str_item)
res1 = baike.search_for_content(str_item)

#%%
baike.get_talents(res)
#%%
>>>>>>> fe9bac6303071d5862f0f30969f5ef0ea1af8a55
pd.read_html(res)