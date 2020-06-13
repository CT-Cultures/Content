# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:04:07 2019

@author: VX
"""
# 保存电影数据分析函数
#%%
# Load Standard Library
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
from urllib.error import HTTPError
import re
import numpy as np
import pandas as pd

# Load from Local
from IO_Storage import File
######################################################################
class GetRegistration(object):
 
    def __init__(self):
        super(GetRegistration, self).__init__()
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        # 电影备案立项网址
        self.url_reg = "http://dy.chinasarft.gov.cn/html/www/catalog/0129dffcccb1015d402881cd29de91ec.html"
        self.path_records = 'records'
        
        
# 抓取现有分页，return 所有分页链接的 tuple
    def links_of_pages(self):
        with urlopen(self.url_reg) as x: 
            html = x.read().decode('utf-8')
        links_allpages = []
        bsObj = BeautifulSoup(html, 'html5lib')
        for item in bsObj.find_all(href=re.compile("pageIndex")):
           links_allpages += (self.url_base + item.get("href"),)
#           print(links_allpages)
        links_allpages = links_allpages[0:-2]# 删除最后两个链接：下一页与最后一页
        links_allpages = pd.DataFrame(links_allpages)
        links_allpages.columns = ['links_of_pages']
        return links_allpages

# 
    def links_of_publications(self, savefile=False):
        links_allpages = self.links_of_pages()
        links_of_publications = []
        for _, each_publish in links_allpages.iterrows():
            with urlopen(each_publish.values[0]) as x: 
                html = x.read()   # site has probelm decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find_all(href=re.compile("blueprint.nsp?")):
#                print(item)
                links_of_publications += [[self.url_base + item.get("href"), str(item.next_element)]]
        links_of_publications = pd.DataFrame(links_of_publications)
        links_of_publications.columns = ['公示批次链接','名称']
        if savefile:
            #writer = File()
            filename = "PubThreatricalRegistration_links_allpublishes.csv"
            links_of_publications.to_csv(self.path_records + '//' + filename)
            #writer.write_to_cvs_wbk(list_links_allpublications, self.path_records, filename)
        return links_of_publications
    
    def links_of_registrations(self, list_links_allpublications, savefile=False, heading=False):
        list_links_allregistrations = []
        if heading:
            heading = ['公示日期', '公示批次名称', '备案详细页链接']
            list_links_allregistrations += [heading]
        url_part_blueprint = '/shanty.deploy/blueprint.nsp?'
        templateId = 'templateId=012a2e051030004740284c812a2d62df'     
        pattern_id = re.compile("id=.*?&")  # 定义查找id的规律 
        for link in list_links_allpublications:
            with urlopen(link[0]) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                title_publish = bsObj.find(class_="heading").get_text()
#                print(title_publish)
                dt_publish = bsObj.find(class_="time").get_text().lstrip(u' 【发布时间】:').rstrip(' ')
#                print(dt_publish)
                for item in bsObj.find_all(["table", "a"], onclick=True):
#                    print(item)
#                    html_review +=(str(item),)
                    str_item = re.sub('\n.*?\n', '', str(item)) # clean spaces and breaks
                    if pattern_id.search(str_item) != None:
                        str_id = pattern_id.search(str_item)[0]
                        clean_char = re.sub("\"", '', str_id)
                        str_id = clean_char
                    else:
                        str_id = '__NO_ID__'
                        print(str_id, ": ")
                        print(title_publish)
                        print(str(len(list_links_allregistrations)), ": ")
                        print("str(item): " + str(item))
                        print("str_item: " + str_item)
                    url_link_reg = self.url_base + url_part_blueprint + str_id + templateId
#                    print(url_link_reg)
                    list_links_allregistrations += [[dt_publish, title_publish, url_link_reg]]
#        print("Total of " + str(len(links_allregistrations)-1) + " registrations links scrapped from web.")
        if savefile:
            writer = File()
            filename = "PubThreatricalRegistration_links_allregistrations"
            writer.write_to_cvs_wbk(list_links_allpublications, self.path_records, filename)
        return list_links_allregistrations
    
    def contents_of_registrations(self, list_links_allregistrations, savefile=False, heading=False):
        list_info_allregistrations = []
        if heading:
            heading = ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接']
            list_info_allregistrations += [heading]
        for link in list_links_allregistrations:
            with urlopen(link[2]) as x:
                html = x.read()
            bsObj_reg = BeautifulSoup(html, 'html.parser')
            table = bsObj_reg.find("table", class_="form") # 读取信息表
            tb_row_second = list()
            tb_row_third= list()                  
            for item in table.find("tr").find_next_sibling("tr").find_all("td"):
                tb_row_second.append(item.get_text().rstrip('\xa0'))
#            print(tb_row_second)
            for item in table.find("tr").find_next_sibling("tr").find_next_sibling("tr").find_all("td"):
                tb_row_third.append(item.get_text().lstrip('\n梗概：').rstrip('\n'))
            tb_row_third.append(link[0])
            tb_row_third.append(link[1])
            tb_row_third.append(link[2])
#            print(tb_row_third)
            info_reg = tb_row_second + tb_row_third
#            print(tb_info_reg)
            list_info_allregistrations += [info_reg]
#        print("Total number of " + str(len(info_allregistrations)-1) + " registration info scrapped from web.")
        if savefile:
            writer = File()
            filename = "PubTheatricalRegistration_info_allregistrations"
            writer.write_to_cvs_wbk(list_info_allregistrations, self.path_records, filename)
        return list_info_allregistrations
    
class UpdateRegistration(object):
    
    def __init__(self):
        super(UpdateRegistration, self).__init__()
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        # 电影备案立项网址
        self.url_reg = "http://dy.chinasarft.gov.cn/html/www/catalog/0129dffcccb1015d402881cd29de91ec.html"
        self.path_records = 'records'
    
    def links_of_newpublications(self, savefile=False):
        GR = GetRegistration()
        # 打开现有存档
        filename = "PubThreatricalRegistration_links_allpublishes"
        reader = File()
        filepath = Path(self.path_records + "\\" + filename + ".csv")
        records_existing = reader.open_to_list_of_list(filepath)
        heading_links_publications = ['公示批次链接','名称']
        if heading_links_publications == records_existing[0]:
            records_existing = records_existing[1:len(records_existing)] #saved records shall have heading, remove heading
        # 网上获取最新
        records_latest = GR.links_of_publications() 
        len_diff= len(records_latest) - len(records_existing)
        list_links_newpublications = []
        if len_diff == 0:
            return list_links_newpublications
        else:
            index = 0
            while index < len_diff:
                list_links_newpublications += [records_latest[index]]
                index = index + 1
            if savefile:
                filename = "PubThreatricalRegistration_links_allpublishes"
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing_linkpub = reader.open_to_list_of_list(filepath)
                if heading_links_publications == records_existing_linkpub[0]:
                    records_existing_linkpub = records_existing_linkpub[1:]
                already_in_record = list(filter(lambda x:x == list_links_newpublications[0], records_existing_linkpub))               
                if not already_in_record:                
                    records_joined_linkpub = [heading_links_publications] + list_links_newpublications + records_existing_linkpub
                    writer = File()
                    writer.write_to_cvs_wbk(records_joined_linkpub, self.path_records, filename)                 
            return list_links_newpublications

    def links_of_newregistrations(self, savefile=False):
        GR = GetRegistration()
        list_links_newpublications = self.links_of_newpublications()
        list_links_newregistrations = []
        if len(list_links_newpublications) != 0:
            list_links_newregistrations = GR.links_of_registrations(list_links_newpublications, heading=False, savefile=False)
            if savefile:
                # 保存链接
                self.links_of_newpublications(savefile=savefile)
                # 保存内容
                reader = File()
                filename = "PubThreatricalRegistration_links_allregistrations"
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing_linkreg = reader.open_to_list_of_list(filepath)
                heading_links_registrations = ['公示日期', '公示批次名称', '备案详细页链接']
                if heading_links_registrations == records_existing_linkreg[0]:
                    records_existing_linkreg = records_existing_linkreg[1:]
                already_in_record = list(filter(lambda x:x == list_links_newregistrations[0], records_existing_linkreg))               
                if not already_in_record:                
                    records_joined_linkreg = [heading_links_registrations] + list_links_newregistrations + records_existing_linkreg
                    writer = File()
                    writer.write_to_cvs_wbk(records_joined_linkreg, self.path_records, filename)                
        return list_links_newregistrations
    
    def contents_of_newregistrations(self, savefile=False):
        links_of_newpublications = self.links_of_newpublications()
        list_info_newregistrations = []
        if len(links_of_newpublications) !=0:
            links_of_newregistrations = self.links_of_newregistrations()
            if len(links_of_newregistrations) != 0:
                GR = GetRegistration()
                list_info_newregistrations = GR.contents_of_registrations(links_of_newregistrations)
                if savefile:
           #       保存 公示批次 链接 + 备案 链接         
                    self.links_of_newregistrations(savefile=savefile)
                    print("Links of Publications updated, added ", len(links_of_newpublications), " record(s).")
                    print("Links of Registrations updated, added ", + len(links_of_newregistrations), " record(s).")
          #       保存 备案 内容
                    reader = File()
                    filename = "PubTheatricalRegistration_info_allregistrations"
                    filepath = Path(self.path_records + "\\" + filename + ".csv")
                    records_existing = reader.open_to_list_of_list(filepath)
                    heading_info_registrations = ['备案立项号','片名','备案单位','编剧','备案结果','备案地','梗概','公示日期','公示批次名','公示批次链接']
                    if heading_info_registrations == records_existing[0]:
                        records_existing = records_existing[1:]            
                    already_in_record = list(filter(lambda x:x == list_info_newregistrations[0], records_existing))
                    if not already_in_record:
                        records_joined = [heading_info_registrations] + list_info_newregistrations + records_existing
                        writer = File()
                        writer.write_to_cvs_wbk(records_joined, self.path_records, filename)
                        print("Contents of Registrations updated, added ", + len(list_info_newregistrations), " record(s).")
        return list_info_newregistrations
#####################################################################################
class GetRelease(object):
    
    def __init__(self):
        super(GetRelease, self).__init__()
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        # 电影备案立项网址
        self.url_release = "http://dy.chinasarft.gov.cn/html/www/catalog/012996c2a84002724028815629965e99.html"
        self.path_records = 'records'
 
# 从 电影局官网 抓取 公示分页 的链接
    def links_of_pages(self):
        try:
            with urlopen(self.url_release) as x: html = x.read().decode('utf-8')
        except HTTPError as e:
            print(e)
        bsObj = BeautifulSoup(html, 'html5lib')
#        print(bsObj)
        links_allpages = []
        for item in bsObj.find_all(href=re.compile("catalog")):
           links_allpages.append(self.url_base + item.get("href"))
        links_allpages = links_allpages[0:-2]# 删除最后两个链接：下一页与最后一页
        return links_allpages
    
    def links_of_publications(self, savefile=False, heading=False):
        # 从 电影局官网 抓取 公映许可证发放 批次页 的 链接
        links_allpages = self.links_of_pages()
        links_allpublications = []
        for each_publication in links_allpages:
            with urlopen(each_publication) as x: 
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                for item in bsObj.find_all("a", title=re.compile("电影公映许可证发放公示")):
                    dt_publish = str(item.previous_element.previous_element.previous_element).lstrip(' ').rstrip(' ') # get_dt
                    links_allpublications += [[self.url_base + item.get("href"), dt_publish]]
        if heading:
            heading_links_publications = ['公映许可证发放公示批次链接', '公示日期']
            links_allpublications = [heading_links_publications] + links_allpublications
        if savefile:
            writer = File()
            filename = "PubThreatricalRelease_links_allpublishes"
            writer.write_to_cvs_wbk(links_allpublications, self.path_records, filename)
        return links_allpublications
        
    def contents_of_publications(self, list_links_allpublications, savefile=False, heading=False):
# 从 电影局官网 抓取 公映许可证发放批次页，从中清理出内容信息
        info_allreleases = []
        heading_links_allpublications = ['公映许可证发放公示批次链接', '公示日期']
        if list_links_allpublications == []:
            return info_allreleases
        elif heading_links_allpublications == list_links_allpublications[0]:
            list_links_allpublications = list_links_allpublications[1:]
        for link in list_links_allpublications:
            with urlopen(link[0]) as x:
                html = x.read()
            bsObj= BeautifulSoup(html, 'html5lib')
            head_title = bsObj.head.title.contents[0].strip('\'')  # 获取批次名称
            head_title = re.sub("制片管理 >> ", "", head_title) # clean 国家新闻出版广电总局——制片管理 >> 2016年电影公映许可证发放公示（国产故事片第十一期）
            #print(head_title)
            dt_publish = link[1].lstrip(' ').rstrip(' ')  # 从分页链接表获取发布时间
            table = bsObj.find("table")
            content_allrows = []
            index_row = 0
            for row in table.find_all("tr"):
                content_perrow = []
                index_row = index_row + 1
                if index_row == 2 :
                    for col in row.find_all("td"):
                        content_perrow.append((col.get_text().lstrip().rstrip()))
                    num_col = len(content_perrow)
                elif index_row > 2:   # 有部分页里面是没有 编码列的
                    for col in row.find_all("td"):
                        content_perrow.append((col.get_text().lstrip().rstrip()))
                    num_col = len(content_perrow)
                    if num_col == 5:
                        content_allrows += ([content_perrow[1], content_perrow[2], content_perrow[3], 
                                             content_perrow[4], head_title, content_perrow[0], link[0], dt_publish],)
                    elif num_col == 4:
                        content_allrows += (['无编码', content_perrow[1], content_perrow[2], 
                                             content_perrow[3], head_title, content_perrow[0], link[0], dt_publish],)    
            info_allreleases = info_allreleases + content_allrows            
        if heading:
            headings_info_allreleases = ['编码','公映证号','片名','第一出品单位','批次名称',
                                         '公示批次中的序号','批次链接','发布日期']
            info_allreleases = [headings_info_allreleases] + info_allreleases
        if savefile:
            writer = File()
            filename = "PubThreatricalRelease_info_allreleases"
            writer.write_to_cvs_wbk(info_allreleases, self.path_records, filename)           
        return info_allreleases
    
class UpdateRelease(object):
    
    def __init__(self):
        super(UpdateRelease, self).__init__()
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        # 电影备案立项网址
        self.url_release = "http://dy.chinasarft.gov.cn/html/www/catalog/012996c2a84002724028815629965e99.html"
        self.path_records = 'records'

    def links_of_newpublications(self, savefile=False):
        GRS = GetRelease()
        # 打开现有存档
        filename = "PubThreatricalRelease_links_allpublishes"
        heading_links_publications = ['公映许可证发放公示批次链接', '公示日期']
        reader = File()
        filepath = Path(self.path_results + "\\" + filename + ".csv")
        records_existing = reader.open_to_list_of_list(filepath)
        if heading_links_publications == records_existing[0]:
            records_existing = records_existing[1:len(records_existing)] #saved records shall have heading, remove heading
        # 网上获取最新
        records_latest = GRS.links_of_publications()
        len_diff= len(records_latest) - len(records_existing)
        list_links_newpublications = []
        if len_diff != 0:
            index = 0
            while index < len_diff:
                list_links_newpublications += [records_latest[index]]
                index = index + 1
            if savefile:
                filename = "PubThreatricalRelease_links_allpublishes"
                reader = File()
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing = reader.open_to_list_of_list(filepath)
                if heading_links_publications == records_existing[0]:
                    records_existing = records_existing[1:]
                already_in_record = list(filter(lambda x:x == list_links_newpublications[0], records_existing))
                if not already_in_record:
                    records_joined = [heading_links_publications] + list_links_newpublications + records_existing
                    writer = File()
                    writer.write_to_cvs_wbk(records_joined, self.path_records, filename)               
        return list_links_newpublications
    
    def contents_of_newpublications(self, savefile=False):
        GRS = GetRelease()                
        list_links_newpublications = self.links_of_newpublications()
        list_contents_newpublications  = []
        if len(list_links_newpublications) != 0:
            list_contents_newpublications = GRS.contents_of_publications(list_links_newpublications)
            headings_info_releases = ['编码','公映证号','片名','第一出品单位','批次名称',
                                      '公示批次中的序号','批次链接','发布日期']
            if savefile:
                self.links_of_newpublications(savefile=savefile)
                print("Links of Release Publications updated, added ", + len(list_links_newpublications), " record(s).")   
                filename = "PubThreatricalRelease_info_allreleases"
                reader = File()
                filepath = Path(self.path_records + "\\" + filename + ".csv")
                records_existing = reader.open_to_list_of_list(filepath)
                if headings_info_releases == records_existing[0]:
                    records_existing = records_existing[1:]
                if len(list_contents_newpublications) != 0:
                    already_in_record = list(filter(lambda x:x == list_contents_newpublications[0], records_existing))
                    if not already_in_record:
                        records_joined = [headings_info_releases] + list_contents_newpublications + records_existing
                        writer = File()
                        writer.write_to_cvs_wbk(records_joined, self.path_records, filename)
                        print("Contents of Release Publications updated, added ", + len(list_contents_newpublications), " record(s).")   
        return list_contents_newpublications