# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 22:00:17 2019

@author: VSurfacePro3
"""
import MovieCN

#%%
reg = MovieCN.Registration()
links_allpages = reg.Getlinks_Pages()

class GET(object):
    def Intheater_Releases(self):
        link = 'https://zgdypw.cn/bits/w/films/pors/export?sort=id,desc'