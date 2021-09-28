# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 02:43:45 2019

@author: VSurfacePro3
"""
import json
import re
import time
from pathlib import Path

import cbooo
#from IO_Storage import File
#%%

#%%
rec = cbooo.Record()
#%%
pages = rec.Query_CN()

film_cn_info_overview = []
for page in pages:
    page_json = json.loads(page)
    if page_json.get('tPage') != 0:
        films = page_json.get('pData')
        for film in films:
            film_overview = [film['ID'],
                             film['MovieName'],
                             film['MovieEnName'],
                             film['releaseYear'],
                             film['BoxOffice']
                             ]
            film_cn_info_overview += [film_overview]
heading = ['ID', 'MovieName', 'MovieEnName', 'releaseYear', 'BoxOffice']
film_cn_info_overview = [heading] + film_cn_info_overview
                               
#%%
filer = File()
#%%
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
folder_path = '\\tostudy\\Effects of Name Change\\FilmNameChange\\'
filename = 'combined_list_wkly_bo_2017'
filer.write_to_cvs_wbk(combined_list_wkly_bo, dir_path, filename)
#%%
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
folder_path = '\\tostudy\\Effects of Name Change\\FilmNameChange\\'
filename = 'films2016id'
file_path = Path(dir_path + folder_path + filename + ".csv")
films2016id = filer.open_to_list(file_path)[1:]

len(films2016id) # 356
combined_list_wkly_bo = []
#%%
i_interval = 5
i_start = 105

while( (i_start+i_interval) < 258):
    list_wkly_bo = rec.wklyBO_by_ID(list_id=films2016id[i_start:i_start+i_interval])
    combined_list_wkly_bo += list_wkly_bo
    time.sleep(60)
    i_start = i_start + 1

#%%
interpreter = cbooo.Interpret()
#list_momentum = interpreter.get_momentum(combined_list_wkly_bo)
list_films_wklybo = interpreter.extract_variables02(combined_list_wkly_bo)

#%%
# Save File
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
folder_path = '\\tostudy\\Effects of Name Change\\FilmNameChange\\'
filename = 'cbo2017xy'
filer.write_to_cvs_wbk(list_films_wklybo, dir_path + folder_path, filename)
#%%
# Save File
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
folder_path = '\\tostudy\\Effects of Name Change\\FilmNameChange\\'
filename = 'cbo2018momentum'
filer.write_to_cvs_wbk(list_momentum, dir_path + folder_path, filename)

#%%
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
filename = 'CBOOO_BO_CN'
filer.write_to_cvs_wbk(film_cn_info_overview, dir_path, filename)
#%%
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results\\tostudy'
filename = ''
exporter.write_to_cvs_in_wholestring(pages, dir_path, filename)
