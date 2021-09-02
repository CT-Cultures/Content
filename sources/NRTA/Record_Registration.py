# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:03:16 2020

@author: CT Cultures
"""
#%%
# Load Standard Library
# Load Standard Library
import os
#from sys import platform
from urllib.request import Request, urlopen
import ssl
#from urllib.error import HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import re
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import datetime
from datetime import date
from datetime import timedelta
import time

# Load from Local
#from IO_Storage import File

######################################################################
class Registration(object):
    
    def __init__(self):
        
        super(Registration, self).__init__()
        
        # 中国电影电子政务平台网址
        self.url_base = "https://dsj.nrta.gov.cn"
        
        # 电影电子政务平台备案公示网址
        self.url_registration = "https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=note&pageIndex=1"
        
        # url_browser head
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # folder for aving logs, relative
        self.path_logs = 'logs'
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()

        # contents of registrations existing

        self.contents_of_registrations_existing =  None


        
    ##########        
    def save_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to csv files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '/' + filename + '.json'
        path_file_bk = self.path_records + '/backup/' + filename + appendix_dt + '.json'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_json(path_file)
        print('file saved to: ' + filename + '.json')
    
    ##########  
    
    def links_of_pages(self,
                       filename: str = "links_of_pages",
                       savefile: bool = False) -> pd.DataFrame:
        """
        
        从 电影局官网 抓取 公示分页 的链接
        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "links_of_pages_releases".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_pages : TYPE
            DESCRIPTION.

        """

        req = Request(url=self.url_registration, headers=self.headers)
        # ctx for expired ssl certificate
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE    
        with urlopen(req, context=ctx) as x: 
            html = x.read().decode('utf-8')
            
        bsObj = BeautifulSoup(html, 'html5lib')
        
       
        str_page_over_total_num_of_pages = bsObj.find('font', class_='page_num_value').text
        total_number_of_pages = int(re.split('\/', str_page_over_total_num_of_pages)[1])
        
        links_of_pages = [self.url_registration]       
        
        for n in range(2, total_number_of_pages+1):
            links_of_pages.append(self.url_registration[:-1] + str(n))
                       
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])

        if savefile:
            self.save_records(links_of_pages, filename, backup=True)
            
        return links_of_pages.copy()
     
    ##########  
       
    def links_of_publications(self, 
                              links_of_pages: pd.DataFrame = 'default',
                              filename: str = 'links_of_publications', 
                              savefile: bool = False) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        links_of_pages : pd.DataFrame, optional
            DESCRIPTION. The default is 'default'.
        filename : str, optional
            DESCRIPTION. The default is "links_of_publications".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # 从 电影局官网 抓取 公映许可证发放 批次页 的 链接
        if links_of_pages == 'default':
            links_of_pages = self.links_of_pages
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        
        links_of_publications = []
        for link_page in self.links_of_pages['links_of_pages'].tolist():
            
            req = Request(url=link_page, headers=self.headers)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE  
            with urlopen(req, context=ctx) as x: 
              html = x.read().decode('utf-8')   # site has problem decoding
              bsObj = BeautifulSoup(html, 'html5lib')
              for item in bsObj.body.find_all('a', target="_blank"):
                  link = self.url_base + '/' + item.get('href')
                  name = item.text
                  links_of_publications.append([link, name])

                
        if len(links_of_publications) > 0:
            links_of_publications = pd.DataFrame(links_of_publications)
            links_of_publications.columns = ['公示批次链接', '公示名称']
        else:
            links_of_publications = pd.DataFrame(columns = ['公示批次链接', '公示名称'])
            
                  
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
            
        return links_of_publications.copy()
    ##########
    def links_of_registrations(self, 
                                 links_of_publications: pd.DataFrame,
                                 filename: str = "links_of_registrations", 
                                 savefile: bool = False) -> pd.DataFrame:

          
        ls_df = []
        for link, name in zip(links_of_publications['公示批次链接'].tolist(), 
                              links_of_publications['公示名称'].tolist()
                             ):
            req = Request(url=link, headers=self.headers) 
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # 2009年3月起
            t  = 0
            with urlopen(req, context=ctx) as x:
                t += 1
                if t % 10 == 0:
                    time.sleep(5)
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                if not bsObj.body.find(text='剧目列表：'):
                    break
                table = bsObj.body.find(text='剧目列表：').next_element.next_element.next_element
                df = pd.read_html(str(table))[0]
                links = []
                for tr in table.findAll("tr"):
                    trs = tr.findAll("td")
                    for each in trs:
                        try:
                            link = each.find('a')['href']
                            links.append(self.url_base + '/' + link)
                        except:
                            pass
                df['备案链接'] = links
                df['公示名称'] = name
                df['公示批次链接'] = link
                ls_df.append(df)
                
        if len(ls_df) != 0:
            links_of_registrations = pd.concat([ls_df[i] for i in range(len(ls_df))], ignore_index=True)
        else:
            links_of_registrations = pd.DataFrame()
            links_of_registrations.columns = ['地区', '剧名', '题材', '制作机构', '备案链接', '公示名称', '公示批次链接']
            
        if savefile:
            self.save_records(links_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
      
        return links_of_registrations
    
    ##########
    def contents_of_registrations(self, 
                                 links_of_registrations: pd.DataFrame,
                                 filename: str = "contents_of_registrations", 
                                 savefile: bool = False) -> pd.DataFrame:
        """
        This Function get the contents of TV registrations

        Parameters
        ----------
        links_of_registrations : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        contents_of_releases : pd.DataFrame
            ['报备机构', '公示年月', '许可证号', '剧名', '题材', 
             '体裁', '集数', '拍摄日期', '制作周期', '内容提要',
             '省级管理部门备案意见', '相关部门意见', '备注'
             ]

        """

        ls_records = []
        i2type = {2: '一般', 3: '喜剧', 4:'戏曲'}
        t  = 0
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        for idx, reg in links_of_registrations.iterrows():
            req = Request(url=reg['备案链接'], headers=self.headers) 
            with urlopen(req, context=ctx) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
    
                record = {'备案链接': reg['备案链接']}
                for i, td in enumerate(bsObj.body.find_all('table')[2].tbody.tr.find_all('td')):
                    if i == 0: record['报备机构'] = re.sub(' ', '', td.text)
                    elif i == 1: record['公示年月'] = re.sub(' ', '', td.text)
                    elif i == 2: record['许可证号'] = re.sub(' ', '', td.text)
                
                for i, tr in enumerate(bsObj.body.find_all('table')[3].tbody.find_all('tr')):
                    if i == 0:
                        for td in tr.find_all('td'):
                            record[td.text] = ''
                    elif i == 2:
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 0: #剧名
                                record['剧名'] = re.sub(' ', '', td.text)
                            elif j == 1: #题材
                                record['题材'] = re.sub(' ', '', td.text)
                            elif j in [2, 3, 4]: #体裁
                                if re.search('√', td.text):
                                    record['体裁'] = i2type[j]
                            elif j == 5: #集数
                                record['集数'] = re.sub(' ', '', td.text)
                            elif j == 6: #拍摄日期
                                 record['拍摄日期'] = re.sub(' ', '', td.text)
                            elif j == 7: #制作周期
                                record['制作周期'] = re.sub(' ', '', td.text)
                    elif i == 3: #内容提要
                        record['内容提要'] =  re.sub(' ', '', tr.td.text)
                    elif i == 4: 
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 1:
                                record['省级管理部门备案意见'] = re.sub(' ', '', td.text)
                            elif j == 3:
                                record['相关部门意见'] = re.sub(' ', '', td.text)
                    elif i == 5: # 备注
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 1:
                                record['备注'] = re.sub(' ', '', td.text)
                ls_records.append(record)
            t += 1
            if t % 50 == 0:
                print('------{}------{}--------'.format(t, record['剧名']))
                time.sleep(5)
            
            if len(ls_records) != 0:
                contents_of_registrations = pd.DataFrame(ls_records)
                contents_of_registrations['许可证号'] = contents_of_registrations['许可证号'].apply(
                    lambda x: x.split('：')[1].lstrip('\n+').lstrip('\t+').rstrip('\t+').rstrip('\n+'))
                contents_of_registrations['报备机构'] = contents_of_registrations['报备机构'].apply(
                    lambda x: x.split('：')[1])
                contents_of_registrations['内容提要'] = contents_of_registrations['内容提要'].apply(
                    lambda x: x.split('：')[1].lstrip('\n+').lstrip('\t+').rstrip('\t+').rstrip('\n+'))
                contents_of_registrations = contents_of_registrations[['剧名', '集数', '报备机构', '题材', '内容提要', 
                                                                '公示年月', '许可证号', '体裁', '拍摄日期', '制作周期', 
                                                                '省级管理部门备案意见', '相关部门意见', '备注'
                                                                ]].copy()
            else:
                contents_of_registrations = pd.DataFrame()
                contents_of_registrations.columns = ['剧名', '集数', '报备机构', '题材', '内容提要', '公示年月', 
                                                     '许可证号', '体裁', '拍摄日期', '制作周期', 
                                                     '省级管理部门备案意见', '相关部门意见', '备注'
                                                     ]
            
        if savefile:
            self.save_records(contents_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
      
        return contents_of_registrations
    
    ##########    
    def update_records(self, 
                       fn_links_of_publications: str = "links_of_publications_releases",
                       fn_contents_of_releases: str = "contents_of_releases",
                       save_update: bool = False
                       ) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        fn_links_of_publications : str, optional
            DESCRIPTION. The default is "links_of_publications_releases".
        fn_contents_of_releases : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        save_update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        # Import Existing Records:
        if os.path.isfile(self.path_records + '//' + fn_links_of_publications + '.json'):
            links_of_publications = pd.read_json(self.path_records + '//' + fn_links_of_publications + '.json', encoding='utf-8-sig')
        else:
            links_of_publications = self.links_of_publications('empty')
        
            
        if os.path.isfile(self.path_records + '//' + fn_contents_of_releases + '.json'):
            contents_of_releases = pd.read_json(self.path_records + '//' + fn_contents_of_releases + '.json', encoding='utf-8-sig')
        else:
            contents_of_releases = self.contents_of_releases(links_of_publications = pd.DataFrame())
        
        links_of_publications_latest = self.links_of_publications()

######################################################################
class Registration(object):
    
    def __init__(self):
        
        super(Registration, self).__init__()
        
        # 中国电影电子政务平台网址
        self.url_base = "https://dsj.nrta.gov.cn"
        
        # 电影电子政务平台备案公示网址
        self.url_registration = "https://dsj.nrta.gov.cn/tims/site/views/applications.shanty?appName=note&pageIndex=1"
        
        # url_browser head
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # folder for aving logs, relative
        self.path_logs = 'logs'
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()
        
        # read existing contents of registrations
        self.contents_of_regstrations_existing = None
        if os.path.isfile(self.path_records + '//'  + 'contents_of_registrations.json'):
            self.contents_of_regstrations_existing = pd.read_json(
                self.path_records + '//'  + 'contents_of_registrations.json')
            
        # read existing links of registraions
        self.links_of_registrations_existing = None
        if os.path.isfile(self.path_records + '//'  + 'links_of_registrations.json'):
            self.links_of_registrations_existing = pd.read_json(
                self.path_records + '//'  + 'links_of_registrations.json')  
        
        # read existing links of publications
        self.links_of_publications_existing = None
        if os.path.isfile(self.path_records + '//'  + 'links_of_publications.json'):
            self.links_of_publications_existing = pd.read_json(
                self.path_records + '//'  + 'links_of_publications.json')  
        


        
    ##########        
    def save_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to csv files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '/' + filename + '.json'
        path_file_bk = self.path_records + '/backup/' + filename + appendix_dt + '.json'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_json(path_file)
        print('file saved to: ' + filename + '.json')
    
    ##########  
    
    def links_of_pages(self,
                       filename: str = "links_of_pages",
                       savefile: bool = False) -> pd.DataFrame:
        """
        
        从 NRTA 抓取 公示分页 的链接
        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "links_of_pages_releases".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_pages : TYPE
            DESCRIPTION.

        """

        req = Request(url=self.url_registration, headers=self.headers)
        # ctx for expired ssl certificate
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE    
        with urlopen(req, context=ctx) as x: 
            html = x.read().decode('utf-8')
            
        bsObj = BeautifulSoup(html, 'html5lib')
        
       
        str_page_over_total_num_of_pages = bsObj.find('font', class_='page_num_value').text
        total_number_of_pages = int(re.split('\/', str_page_over_total_num_of_pages)[1])
        
        links_of_pages = [self.url_registration]       
        
        for n in range(2, total_number_of_pages+1):
            links_of_pages.append(self.url_registration[:-1] + str(n))
                       
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])

        if savefile:
            self.save_records(links_of_pages, filename, backup=True)
            
        return links_of_pages.copy()
     
    ##########  
       
    def links_of_publications(self, 
                              links_of_pages: pd.DataFrame = 'default',
                              filename: str = 'links_of_publications',
                              ignore_old: bool = False,
                              savefile: bool = False) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        links_of_pages : pd.DataFrame, optional
            DESCRIPTION. The default is 'default'.
        filename : str, optional
            DESCRIPTION. The default is 'links_of_publications'.
        ignore_old : bool, optional
            DESCRIPTION. The default is True.
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        # NRTA链接
        if links_of_pages == 'default':
            links_of_pages = self.links_of_pages
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        
        links_of_publications = []
        for link_page in self.links_of_pages['links_of_pages'].tolist():
            
            req = Request(url=link_page, headers=self.headers)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE  
            with urlopen(req, context=ctx) as x: 
              html = x.read().decode('utf-8')   # site has problem decoding
              bsObj = BeautifulSoup(html, 'html5lib')
              for item in bsObj.body.find_all('a', target="_blank"):
                  link = self.url_base + '/' + item.get('href')
                  name = item.text
                  links_of_publications.append([link, name])

                
        if len(links_of_publications) > 0:
            links_of_publications = pd.DataFrame(links_of_publications)
            links_of_publications.columns = ['公示批次链接', '公示名称']
            # Import pub to disregard
            S_pub_to_ignore = pd.read_json('S_pub_to_disregard.json', orient='index')
            ls_pub_to_ignore = S_pub_to_ignore[0].tolist()
            if ignore_old:
                links_of_publications = links_of_publications[
                    ~links_of_publications['公示名称'].isin(ls_pub_to_ignore)]
        else:
            links_of_publications = pd.DataFrame(columns = ['公示批次链接', '公示名称'])
            
                  
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
            
        return links_of_publications.copy()
    ##########
    def links_of_registrations(self, 
                                 links_of_publications: pd.DataFrame,
                                 filename: str = "links_of_registrations", 
                                 savefile: bool = False) -> pd.DataFrame:

          
        ls_df = []
        for link, name in zip(links_of_publications['公示批次链接'].tolist(), 
                              links_of_publications['公示名称'].tolist()
                             ):
            req = Request(url=link, headers=self.headers) 
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            # 2009年3月起
            t  = 0
            with urlopen(req, context=ctx) as x:
                t += 1
                if t % 10 == 0:
                    time.sleep(5)
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                if not bsObj.body.find(text='剧目列表：'):
                    break
                table = bsObj.body.find(text='剧目列表：').next_element.next_element.next_element
                df = pd.read_html(str(table))[0]
                links = []
                for tr in table.findAll("tr"):
                    trs = tr.findAll("td")
                    for each in trs:
                        try:
                            link = each.find('a')['href']
                            links.append(self.url_base + '/' + link)
                        except:
                            pass
                df['备案链接'] = links
                df['公示名称'] = name
                df['公示批次链接'] = link
                ls_df.append(df)
                
        if len(ls_df) != 0:
            links_of_registrations = pd.concat([ls_df[i] for i in range(len(ls_df))], ignore_index=True)
        else:
            links_of_registrations = pd.DataFrame()
            links_of_registrations.columns = ['地区', '剧名', '题材', '制作机构', '备案链接', '公示名称', '公示批次链接']
            
        if savefile:
            self.save_records(links_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
      
        return links_of_registrations
    
    ##########
    def contents_of_registrations(self, 
                                 links_of_registrations: pd.DataFrame,
                                 filename: str = "contents_of_registrations", 
                                 savefile: bool = False) -> pd.DataFrame:
        """
        This Function get the contents of TV registrations

        Parameters
        ----------
        links_of_registrations : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        contents_of_releases : pd.DataFrame
            ['报备机构', '公示年月', '许可证号', '剧名', '题材', 
             '体裁', '集数', '拍摄日期', '制作周期', '内容提要',
             '省级管理部门备案意见', '相关部门意见', '备注'，
             '备案链接', '公示名称', '公示批次链接', ''地区''
             ]

        """

        ls_records = []
        i2type = {2: '一般', 3: '喜剧', 4:'戏曲'}
        t  = 0
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        for idx, reg in links_of_registrations.iterrows():
            req = Request(url=reg['备案链接'], headers=self.headers) 
            with urlopen(req, context=ctx) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
    
                record = {'备案链接': reg['备案链接'],
                          '公示名称':  reg['公示名称'],
                          '公示批次链接': reg['公示批次链接'],
                          '地区': reg['地区']
                          }
                        
                for i, td in enumerate(bsObj.body.find_all('table')[2].tbody.tr.find_all('td')):
                    if i == 0: record['报备机构'] = re.sub(' ', '', td.text)
                    elif i == 1: record['公示年月'] = re.sub(' ', '', td.text)
                    elif i == 2: record['许可证号'] = re.sub(' ', '', td.text)
                
                for i, tr in enumerate(bsObj.body.find_all('table')[3].tbody.find_all('tr')):
                    if i == 0:
                        for td in tr.find_all('td'):
                            record[td.text] = ''
                    elif i == 2:
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 0: #剧名
                                record['剧名'] = re.sub(' ', '', td.text)
                            elif j == 1: #题材
                                record['题材'] = re.sub(' ', '', td.text)
                            elif j in [2, 3, 4]: #体裁
                                if re.search('√', td.text):
                                    record['体裁'] = i2type[j]
                            elif j == 5: #集数
                                record['集数'] = re.sub(' ', '', td.text)
                            elif j == 6: #拍摄日期
                                 record['拍摄日期'] = re.sub(' ', '', td.text)
                            elif j == 7: #制作周期
                                record['制作周期'] = re.sub(' ', '', td.text)
                    elif i == 3: #内容提要
                        record['内容提要'] =  re.sub(' ', '', tr.td.text)
                    elif i == 4: 
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 1:
                                record['省级管理部门备案意见'] = re.sub(' ', '', td.text)
                            elif j == 3:
                                record['相关部门意见'] = re.sub(' ', '', td.text)
                    elif i == 5: # 备注
                        for j, td in enumerate(tr.find_all('td')):
                            if j == 1:
                                record['备注'] = re.sub(' ', '', td.text)
                ls_records.append(record)
            t += 1
            if t % 50 == 0:
                print('------{}------{}--------'.format(t, record['剧名']))
                time.sleep(5)
            
            if len(ls_records) != 0:
                contents_of_registrations = pd.DataFrame(ls_records)
                contents_of_registrations['许可证号'] = contents_of_registrations['许可证号'].apply(
                    lambda x: x.split('：')[1].lstrip('\n+').lstrip('\t+').rstrip('\t+').rstrip('\n+'))
                contents_of_registrations['报备机构'] = contents_of_registrations['报备机构'].apply(
                    lambda x: x.split('：')[1])
                contents_of_registrations['内容提要'] = contents_of_registrations['内容提要'].apply(
                    lambda x: x.split('：')[1].lstrip('\n+').lstrip('\t+').rstrip('\t+').rstrip('\n+'))
                contents_of_registrations = contents_of_registrations[[
                    '剧名', '集数', '报备机构', '题材', '内容提要', 
                    '公示年月', '许可证号', '体裁', '拍摄日期', '制作周期', 
                    '省级管理部门备案意见', '相关部门意见', '备注', 
                    '备案链接', '公示名称', '公示批次链接', '地区'
                    ]].copy()
            else:
                contents_of_registrations = pd.DataFrame()
                contents_of_registrations.columns = [
                    '剧名', '集数', '报备机构', '题材', '内容提要', '公示年月', 
                    '许可证号', '体裁', '拍摄日期', '制作周期', 
                    '省级管理部门备案意见', '相关部门意见', '备注',
                    '备案链接', '公示名称', '公示批次链接', '地区'
                    ]
            
        if savefile:
            self.save_records(contents_of_registrations, filename, backup=True)
            print(filename + '.json updated.')
      
        return contents_of_registrations
    
    ##########    
    def update_records(self, 
                       fn_links_of_publications: str = "links_of_publications_releases",
                       fn_contents_of_registrations: str = "contents_of_registrations",
                       save_update: bool = False
                       ) -> pd.DataFrame:
        """
        

        Parameters
        ----------
        fn_links_of_publications : str, optional
            DESCRIPTION. The default is "links_of_publications_releases".
        fn_contents_of_releases : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        save_update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        
        
        # Import Existing Records:
        if os.path.isfile(self.path_records + '//' + fn_links_of_publications + '.json'):
            links_of_publications = pd.read_json(self.path_records + '//' + fn_links_of_publications + '.json', encoding='utf-8-sig')
        else:
            links_of_publications = self.links_of_publications('empty')
        
            
        if os.path.isfile(self.path_records + '//' + fn_contents_of_releases + '.json'):
            contents_of_releases = pd.read_json(self.path_records + '//' + fn_contents_of_releases + '.json', encoding='utf-8-sig')
        else:
            contents_of_releases = self.contents_of_releases(links_of_publications = pd.DataFrame())
        
        links_of_publications_latest = self.links_of_publications()
        