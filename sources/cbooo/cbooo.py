# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 00:13:51 2019

@author: VSurfacePro3
"""
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
from urllib.error import HTTPError
from selenium import webdriver
import json
import datetime
import re
import time

# Load from Local
from IO_Storage import File
from CrawlCleaner import ChineseCleaner
#%%
class Record(object):
    
    def __init__(self):
        if not self:
            raise ValueError
            
    def Query_CN(self):
        para = Parameter()
        area = 50
        initials = para.initials() #list of string
        #initials = ['A', 'B']
        years = para.years()
        #years = [2015, 2016, 2017, 2018, 2019]
        #years = [2015]
        pages = []
        for year in years:
            for initial in initials:
                page_first = self.Search_firstpage(area=area, year=str(year), initial=initial)
                tPage = page_first[1]
                pages += [page_first[0]]
                i = 2
                while i <= int(tPage):
                    page = self.Search(area=area, year=str(year), initial=initial, pIndex=i)
                    pages += [page]
                    i += 1
        return pages
                
    
    def Search_firstpage(self, area=50, stype=0, year=0, initial='A', pIndex=1):
        url_root = 'http://www.cbooo.cn/'
        url_searchpath = '/Mdata/getMdata_movie'
        url_search = (url_root + url_searchpath
                      + '?area=' + str(area) + '&'
                      + 'type=' + str(stype) + '&'
                      + 'year=' + str(year) + '&'
                      + 'initial=' + str(initial) + '&'
                      + 'pIndex=' + str(pIndex)
                      )
        print(url_search)
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        driver.get(url_search)
        driver.implicitly_wait(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html5lib')
        page_json = soup.pre.get_text()
        job = json.loads(page_json)
        tPage = job.get('tPage')
        #item_count_total = job.get('tCount')
        page_w_tpagecount = [page_json, tPage]
        driver.close()
        return page_w_tpagecount
        
    def Search(self, area=50, stype=0, year=0, initial='A', pIndex=1):
        url_root = 'http://www.cbooo.cn/'
        url_searchpath = '/Mdata/getMdata_movie'
        url_search = (url_root + url_searchpath
                      + '?area=' + str(area) + '&'
                      + 'type=' + str(stype) + '&'
                      + 'year=' + str(year) + '&'
                      + 'initial=' + str(initial) + '&'
                      + 'pIndex=' + str(pIndex)
                      ) 
        print(url_search)
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        driver.get(url_search)
        driver.implicitly_wait(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html5lib')
        page_json = soup.pre.get_text()
        driver.close()
        return page_json
    
    def wklyBO_by_ID(self, list_id=['589946', '612645', '672563']):
        #list_id = ["589946", "612645", "672563"]
        url_root = 'http://www.cbooo.cn/'
        url_searchpath = '/m/'
        chromeoptions = webdriver.chrome.options.Options()
        chromeoptions.headless = True
        driver = webdriver.Chrome(options = chromeoptions)
        bo_wkly = []
        heading = ['上映周', '均场人次', '单周票房（万）', '累计票房（万）', '上映天数']
        clean = ChineseCleaner()
        for num_id in list_id:
            url_search = (url_root + url_searchpath + num_id)
            print(url_search)
            driver.get(url_search)
            driver.implicitly_wait(10)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html5lib')
            part_title = soup.head.title.get_text()
            if part_title == " - 我的 ASP.NET MVC 应用程序":
                continue
            part_tabcont2 = soup.find(attrs={"id": "tabcont2"})
            #print(part_tabcont2)                     
            part_td = part_tabcont2.find_all("td")
            pattern_text = '第[0-9].*周[0-9][0-9][0-9][0-9]年'
            pattern = re.compile(pattern_text)
            rec_wkly = []
            count = 0
            rec_row = []
            for item in part_td:
                #print (item.get_text())
                if pattern.search(item.get_text()):
                    count += 1
                    if count > 1:
                        rec_wkly += [rec_row]
                        rec_row = []
                        #print(rec_wkly)
                    rec_row.append(clean.Clean_Numbers(item.get_text()))
                else:
                    rec_row.append(clean.Clean_Numbers(item.get_text()))
                    #print(item.get_text())
            rec_wkly += [rec_row]
            rec_wkly = [num_id] + [rec_wkly]
            print(rec_wkly)
            bo_wkly += [rec_wkly]
            time.sleep(7)
        driver.close()
        return bo_wkly
    
    
#    def event_by_ID(self, num_id=""):
        #http://www.cbooo.cn/Mdata/getMovieEventAll?movieid=589946
        
###############################################################################
class Update(object):
    
    def __init__(self):
        if not self:
            raise ValueError
    
    def records(self):
        para = Parameter()
        area = 50
        initials = para.initials() #list of string
        #initials = ['A', 'B']
        years = para.years()
        #years = [2015, 2016, 2017, 2018, 2019]
        #years = [2015]
        pages = []
###############################################################################
class Parameter(object):
     
    def __init__(self):
        if not self:
            raise ValueError
    
    def initials(self):
        letters =['A', 'B', 'C', 'D', 'E', 'F', 'G',
                  'H', 'I', 'J', 'K', 'L', 'M', 'N',
                  'O', 'P', 'Q', 'R', 'S', 'T', 
                  'U', 'V', 'W', 'X', 'Y', 'Z']
        return letters
    
    def years(self):
        current_year = datetime.datetime.now().year
        years = list(range(1949,current_year+1))
#        years = list(range(2008,current_year+1))      
        years = list(sorted(years, reverse=True))
        return years
    
    def areas(self):
        areas = {50:r'中国', 37:r'中国香港', 40:r'中国台湾',
                 1:r'美国' , 25:r'英国'    , 16:r'德国',
                 4:r'法国' , 30:r'日本'    , 2:r'加拿大',
                 7:r'意大利', 
                 }
#%%
###############################################################################
class Interpret(object):
     
    def __init__(self):
        if not self:
            raise ValueError
            
    def extract_variables04(self, combined_list_wkly_bo):
        heading = ["ID", "Name", "X", "y"]
        ###
        filer = File()
        dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
        filename = 'CBOOO_BO_CN'
        file_path = Path(dir_path + "\\" + filename + ".csv")
        cbo_records = filer.open_to_list_of_list(file_path)  
        ###
        list_films_wklybo = []
        for item in combined_list_wkly_bo:
            id_film = item[0]
            x = []
            y = []
            if item[1] != [[]]:
                wks_all = item[1]
                for wk in wks_all:
                    dt_range = wk[0]
                    ppl_per_hall = int(wk[1])
                    bo_wk = int(wk[2])
                    bo_wk_cumulative = int(wk[3])
                    if len(wk) > 4:
                        num_days = int(wk[4])
                        x.append(num_days)
                        y.append(bo_wk_cumulative)
                    else:
                        x.append(0)
                        y.append(bo_wk_cumulative)
            for record in cbo_records:
                if record[0] == id_film:
                    num_days_max = 7
                    if (x != [] and x[0] < 23):
                        num_days_max = x[0] + 7
                    elif (x !=[] and x[0] >= 23 and x[0] < 31):
                        num_days_max = 31
                    elif (x !=[] and x[0] >= 31 and x[0] < 53):
                        num_days_max = x[0] + 7
                    elif (x !=[] and x[0] >= 53 and x[0] < 62):
                        num_days_max = 62
                    else:
                        num_days_max = x[0] + 7
                    bo_final = int(record[4])
                    x = [num_days_max] + x
                    y = [bo_final] + y
                    break
            index = 0
            while (index < len(x)):
                list_films_wklybo += [[id_film, record[1], x[index], y[index]]]
                index += 1
        list_films_wklybo = [heading] + list_films_wklybo
        return list_films_wklybo
            
    def extract_variables02(self, combined_list_wkly_bo):
        heading = ["ID", "Name", "X", "y"]
        ###
        filer = File()
        dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
        filename = 'CBOOO_BO_CN'
        file_path = Path(dir_path + "\\" + filename + ".csv")
        cbo_records = filer.open_to_list_of_list(file_path)  
        ###
        list_films_wklybo = []
        for item in combined_list_wkly_bo:
            id_film = item[0]
            x = []
            y = []
            if item[1] != [[]]:
                wks_all = item[1]
                for wk in wks_all:
                    dt_range = wk[0]
                    ppl_per_hall = int(wk[1])
                    bo_wk = int(wk[2])
                    bo_wk_cumulative = int(wk[3])
                    if len(wk) > 4:
                        num_days = int(wk[4])
                        x.append(num_days)
                        y.append(bo_wk_cumulative)
                    else:
                        x.append(0)
                        y.append(bo_wk_cumulative)
            for record in cbo_records:
                if record[0] == id_film:
                    num_days_max = 30
                    if (x != [] and x[0] > 31):
                        num_days_max = 60
                        if x[0] > 60:
                            num_days_max = 90
                    bo_final = int(record[4])
                    x = [num_days_max] + x
                    y = [bo_final] + y
                    break
            index = 0
            while (index < len(x)):
                list_films_wklybo += [[id_film, record[1], x[index], y[index]]]
                index += 1
        list_films_wklybo = [heading] + list_films_wklybo
        return list_films_wklybo

    def extract_variables01(self, combined_list_wkly_bo):
        heading = ["ID", "Name", "list_days", "list_bo_cumulative"]
        ###
        filer = File()
        dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
        filename = 'CBOOO_BO_CN'
        file_path = Path(dir_path + "\\" + filename + ".csv")
        cbo_records = filer.open_to_list_of_list(file_path)  
        ###
        list_films_wklybo = []
        for item in combined_list_wkly_bo:
            id_film = item[0]
            x = []
            y = []
            if item[1] != [[]]:
                wks_all = item[1]
                for wk in wks_all:
                    dt_range = wk[0]
                    ppl_per_hall = int(wk[1])
                    bo_wk = int(wk[2])
                    bo_wk_cumulative = int(wk[3])
                    if len(wk) > 4:
                        num_days = int(wk[4])
                        x.append(num_days)
                        y.append(bo_wk_cumulative)
                    else:
                        continue
            for record in cbo_records:
                if record[0] == id_film:
                    num_days_max = 30
                    if (x != [] and x[0] > 31):
                        num_days_max = 60
                        if x[0] > 60:
                            num_days_max = 90
                    bo_final = int(record[4])
                    x = [num_days_max] + x
                    y = [bo_final] + y
                    break
            list_films_wklybo += [[id_film, record[1], tuple(x), tuple(y)]]
        #list_films_wklybo = [heading] + list_films_wklybo
        return list_films_wklybo

    def extract_variables03(self, combined_list_wkly_bo):
        heading = ["ID", "Name", "list_days", "list_bo_cumulative"]
        ###
        filer = File()
        dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
        filename = 'CBOOO_BO_CN'
        file_path = Path(dir_path + "\\" + filename + ".csv")
        cbo_records = filer.open_to_list_of_list(file_path)  
        ###
        list_films_wklybo = []
        for item in combined_list_wkly_bo:
            id_film = item[0]
            x = []
            y = []
            if item[1] != [[]]:
                wks_all = item[1]
                for wk in wks_all:
                    dt_range = wk[0]
                    ppl_per_hall = int(wk[1])
                    bo_wk = int(wk[2])
                    bo_wk_cumulative = int(wk[3])
                    if len(wk) > 4:
                        num_days = int(wk[4])
                        x.append(num_days)
                        y.append(bo_wk_cumulative)
                    else:
                        continue
            for record in cbo_records:
                if record[0] == id_film:
                    num_days_max = 30
                    if (x != [] and x[0] > 31):
                        num_days_max = 60
                        if x[0] > 60:
                            num_days_max = 90
                    bo_final = int(record[4])
                    x = [num_days_max] + x
                    y = [bo_final] + y
                    break
            list_films_wklybo += [[id_film, record[1], tuple(x), tuple(y)]]
        #list_films_wklybo = [heading] + list_films_wklybo
        return list_films_wklybo
    
    def get_momentum(self, list_wkly_bo):
        filer = File()
        dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
        filename = 'CBOOO_BO_CN'
        file_path = Path(dir_path + "\\" + filename + ".csv")
        cbo_records = filer.open_to_list_of_list(file_path)
        ####
        initial_days = 7
        list_momentum = []
        for item in list_wkly_bo:
            id_film = item[0]
            num_wk_in_theater = len(item[1])
            if (num_wk_in_theater > 0 and item[1] != [[]]):
                wks_all = item[1]
                # first week 
                #print(wks_all[num_wk_in_theater-1])
                bo_week01 = int(wks_all[num_wk_in_theater-1][2])
                if (len(wks_all[num_wk_in_theater-1]) < 5):
                    wks_week01 = 1
                else:
                    days_week01 = int(wks_all[num_wk_in_theater-1][4])
                if days_week01 ==0: days_week01 = 1
                bo_week01_avg = bo_week01 / days_week01                
                if (days_week01 < initial_days and num_wk_in_theater > 1):
                    bo_week02 = int(wks_all[num_wk_in_theater-2][2])
                    if (len(wks_all[num_wk_in_theater-2]) < 5):
                         wks_week02 = 1
                    else:
                        days_week02 = int(wks_all[num_wk_in_theater-2][4]) - days_week01
                    if days_week02 ==0: days_week02 = 1
                    bo_week02_avg = bo_week02 / days_week02
                    if ( (days_week01+days_week02) < initial_days and num_wk_in_theater > 2):
                        bo_week03 = int(wks_all[num_wk_in_theater-3][2])
                        if (len(wks_all[num_wk_in_theater-3]) < 5):
                            wks_week03 = 1
                        else:
                            days_week03 = int(wks_all[num_wk_in_theater-3][4]) - days_week02 - days_week01
                        if days_week03 ==0: days_week03 = 1
                        bo_week03_avg = bo_week03 / days_week03
                        if( (days_week03+days_week02+days_week01) < initial_days and num_wk_in_theater >3):
                            bo_week04 = int(wks_all[num_wk_in_theater-4][2])
                            if (len(wks_all[num_wk_in_theater-4]) < 5):
                                days_week04 = 1
                            else:
                                days_week04 = int(wks_all[num_wk_in_theater-4][4])- days_week03 - days_week02 - days_week01
                            if days_week04==0: days_week04 = 1
                            bo_week04_avg = bo_week04 / days_week04
                            momentum = bo_week01 + bo_week02 + bo_week03 + bo_week04_avg*(initial_days-days_week03-days_week02-days_week01)
                        else:
                            momentum = bo_week01 + bo_week02 + bo_week03_avg*(initial_days-days_week02-days_week01)
                            list_momentum += [[id_film, momentum]]
                    else:
                        momentum = bo_week01 + bo_week02_avg*(initial_days-days_week01)
                        list_momentum += [[id_film, momentum]]
                else:
                    momentum = bo_week01_avg * days_week01
                    list_momentum += [[id_film, momentum]]
            else:
                for record in cbo_records:
                    if record[0] == id_film:
                        momentum = int(record[4])
                        list_momentum += [[id_film, momentum]]
                        break
        print(list_momentum)
        return(list_momentum)

