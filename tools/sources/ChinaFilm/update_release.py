# -*- coding: utf-8 -*-
"""
Created on Mon May 31 20:24:52 2021

@author: VXhpUS
"""
# Load Libraries
#import argparse
from Record_Release import Release

dy_rel = Release()
#%%
links_of_publications = dy_rel.links_of_publications(savefile=True)
contents_of_releases = dy_rel.contents_of_releases(links_of_publications, savefile=True)
