# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:16:25 2019

@author: VX
"""
#%%
import csv
import os
from pathlib import Path
import datetime
import urllib
import cv2
import numpy as np
import pandas as pd

#%%#%%
class File(object):
    
    def __init__(self):
        if not self:
            raise ValueError

# 从 CVS 导入表格成  Tuple of List （[],[],[])
    def open_to_tuple(self, filepath):
        if filepath.exists():
            items = ()
        with open(filepath, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file, dialect='excel')
            for row in reader:
                items += (str(row).lstrip('\'[').rstrip(']\''),)
            file.close()
        return items
    
    def open_to_list(self, filepath):
        if filepath.exists():
            items = []
        with open(filepath, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file, dialect='excel')
            for row in reader:
                items += [str(row).lstrip('\'[').rstrip(']\'')]
            file.close()
        return items  
    
    def open_to_tuple_of_list(self, filepath):
        if filepath.exists():
            items = ()
        with open(filepath, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file, dialect='excel')
            for row in reader:
                items += (row,)
            file.close()
        return items

    def open_to_list_of_list(self, filepath):
        if filepath.exists():
            items = []
        with open(filepath, newline='', encoding='utf-8-sig') as file:
            reader = csv.reader(file, dialect='excel')
            for row in reader:
                items += [row]
            file.close()
        return items         
    
# 从 CVS 导入表格成  Dictionary （'':'', '':'', '':'')
    def open_to_dict(self, filepath):
        if filepath.exists():
            items = ()
        with open(filepath, newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, dialect='excel')
            for row in reader:
                    items += (str(row).lstrip('\'[').rstrip(']\''),)
            file.close()
        return items
    
    def write_to_cvs(self, content, dir_root, str_filename):
#        tzone_offset = time.timezone
        path_file = dir_root + '\\' + str_filename + '.csv' 
        with open(Path(path_file), 'w', newline='', encoding='utf-8-sig') as output:
            writer = csv.writer(output, dialect = 'excel')
            for item in content:
                writer.writerow(item)
        output.close()
        
    def write_to_cvs_wbk(self, content, dir_root, str_filename):
#        dir_root = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
#        str_filename = "PubThreatricalRegistration_links_allpublishes"
        path_file = dir_root + '\\' + str_filename + '.csv'
#        tzone_offset = time.timezone
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))        
        path_file_bk = dir_root + '\\backup\\' + str_filename + appendix_dt + '.csv'
        if os.path.isfile(path_file):
            os.rename(path_file, path_file_bk)
            with open(Path(path_file), 'w', newline='', encoding='utf-8-sig') as output:
                writer = csv.writer(output, dialect = 'excel')
                for item in content:
                    writer.writerow(item)
                output.close()
        else:
            with open(Path(path_file), 'w', newline='', encoding='utf-8-sig') as output:
                writer = csv.writer(output, dialect = 'excel')
                for item in content:
                    writer.writerow(item)
                output.close()

    def write_to_cvs_in_wholestring(self, content, dir_root, str_filename):
        path_file = dir_root + '\\' + str_filename + '.csv' 
        #dt = datetime.datetime.now()
        #appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))
        with open(Path(path_file), 'w', newline='', encoding='utf-8-sig') as output:
            writer = csv.writer(output, dialect = 'excel')
            for item in content:
                writer.writerow([item])
        output.close()
        
    def web_save_image(self, url_img, dir_source='', dir_project=''):
#        url_img = "https://pixabay.com/get/e832b4092af3053ed1584d05fb1d4590e674e7d418ac104490f4c77ca1eeb1b1_1280.jpg"
#        dir_source = 'Pixabay'
#        dir_project = ''
        rq = urllib.request.Request(url_img)
        rq.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
        rq.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3") 
        url_response = urllib.request.urlopen(rq)
        img = urllib.request.urlopen(rq) 
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        dir_root = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
        if not os.path.isdir(dir_root + "\\" + dir_source):
            os.mkdir(dir_root + "\\" + dir_source)
        if not os.path.isdir(dir_root + "\\" + dir_source + "\\" + dir_project):
            os.mkdir(dir_root + "\\" + dir_source + "\\" + dir_project)
        name_img = url_img.lstrip('https://pixabay.com/get/')
        str_path_img = dir_root + "\\" + dir_source + "\\" + dir_project + "\\" + name_img
#        print(str_path_img)
#        cv2.imshow('image', img)
#        cv2.waitKey(0) & 0xFF
        return cv2.imwrite(str_path_img, img)
######################################################################