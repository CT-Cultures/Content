# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:08:47 2019

@author: VSurfacePro3
"""
# Load Standard Library
import time
import json
import re
from urllib.request import urlopen

# Load from CTAI
from IO_Storage import File

#%%
#https://pixabay.com/api/?key=3653511-527395e146c26edb345843669&q=yellow+flowers&image_type=photo
class Pixabay(object):
    
    def __init__(self, 
                 lang= 'en',
                 image_type = 'all',
                 orientation='all',
                 category = 'all',
                 safesearch = 'false'
                 order = 'popular',
                 page = 1,
                 per_page = 3,
                 pretty = 'false'
                ):
        super(Pixabay, self).__init__()
        self.link_api = 'https://pixabay.com/api/'
        self.apikey = '3653511-527395e146c26edb345843669'
        self.lang = lang
        self.image_type = image_type
        self.orientation = orientation
        self.category = category
        self.safesearch = safesearch
        self.order = order
        self.page = page
        self.per_page = per_page
        self.pretty = pretty
        self.path_save = 'saved_images'
    
    def search(self, keywords: List(), dir_project=''):
        '''This function searches pictures on Pixabay by keywords
        @param List（str): A list of keywords
        @path_project str: for separating saves into folders
        '''
        str_search_pt1 = self.link_api + '?key=' + self.apikey + '&q='
        str_search_pt3 = '&image_type=' + self.image_type + '&per_page=' + str(self.per_page)
       
        pacing = 0 # for controlling saving frequency to avoid api overload
        imagesaver = File()
        for keyword in list_keywords:
            keyword = re.sub(' ', '+', keyword)
            str_search = str_search_pt1 + keyword + str_search_pt3
            response = urlopen(str_search).read().decode('utf-8')
            jsonObj = json.loads(response)
            for image in jsonObj.get('hits'):
                url_img = (image['largeImageURL'])
                imagesaver.web_save_image(url_img, self.path_save, dir_project='SR')
                time.sleep(5)               
            pacing = pacing + 1
            if (pacing % 3) ==0:
                time.sleep(5)       
    
    def searchvideo(self, list_keywords, dir_project=''):
        videosaver = File()
        
    
#%%
#pb = Pixabay()
#list_keywords = ['Vesta','Burning Planet']
#pb.search(list_keywords, dir_project='SR')

