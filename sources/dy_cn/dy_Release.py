# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:03:16 2020

@author: CT Cultures
"""
#%%
# Load Standard Library
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
from urllib.error import HTTPError
import re
import numpy as np
import pandas as pd

import datetime
from pathlib import Path
import os

# Load from Local
from IO_Storage import File

######################################################################
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