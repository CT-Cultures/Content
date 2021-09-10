# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:04:07 2019

@author: VX
"""
# 保存电影数据分析函数
#%%
# Load Standard Library
import os
#from sys import platform
from urllib.request import Request, urlopen
#from urllib.error import HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup

import re
import numpy as np
import pandas as pd
from pandas.tseries.offsets import MonthEnd
import datetime
from datetime import date
from datetime import timedelta

import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
######################################################################
class Registration(object):
 
    def __init__(self, driver=None):
        """
        """
        super(Registration, self).__init__()
        
        # 中国电影政务平台网址
        self.url_base = "http://www.chinafilm.gov.cn"
        
        # 电影备案立项网址
        self.url_reg = "http://www.chinafilm.gov.cn/chinafilm/channels/167.shtml"
        
        # url_browser head
        self.headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # folder for aving logs, relative
        self.path_logs = 'logs'
        
        # links of pages from web
        self.links_of_pages_latest = self.links_of_pages()
        
        # Call Parser Class
        self.parser = Parser_Registration()
        
        # Call Estimate Class
        self.estimate = Estimate_Registration()
        
        if not driver:
            # Load Chrome Driver for AJAX Response Scrapping
            chromeoptions = webdriver.chrome.options.Options()
            chromeoptions.add_argument('--headless')
            chromeoptions.add_argument('--no-sandbox')
            chromeoptions.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(options=chromeoptions)
        else:
            self.driver = driver 
        
        self.links_of_publications_existing = pd.DataFrame()
        self.links_of_registrations_existing = pd.DataFrame()
        self.contents_of_registratons_existing = pd.DataFrame()
        if os.path.isfile(self.path_records + '//' + 'links_of_publications.json'):
           self.links_of_publications_existing = pd.read_json(
               self.path_records + '//' + 'links_of_publications.json')       
        if os.path.isfile(self.path_records + '//' + 'links_of_registrations.json'):
            self.links_of_registrations_existing = pd.read_json(
                self.path_records + '//' + 'links_of_registrations.json')
        if os.path.isfile(self.path_records + '//' + 'contents_of_registrations.json'):
            self.contents_of_registrations_existing = pd.read_json(
                self.path_records + '//' + 'contents_of_registrations.json')
        
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
        print('file saved to: ' + filename + '.json with a total of ', 
              records.shape[0], ' records.')
        
##########
    def append_records(self,
                     records: pd.DataFrame, 
                     filename: str, 
                     backup: bool = False) -> None:
        """
        This functions saves pd.DataFrame to csv files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_' + str(dt.strftime("%Y%m%d")) + '_'+ str(dt.strftime("%H%M"))      
        path_file = self.path_records + '/' + filename + '.csv'
        path_file_bk = self.path_records + '/backup/' + filename + appendix_dt + '.csv'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_csv(path_file, mode='a', header=(not os.path.exists(path_file)), encoding='utf-8-sig', index=False)
        print(records.shape[0], ' records appended to: ' + filename + '.csv')

##########
    def remove_bom_utf8(self, x: str)-> str:
        """
        Parameters
        ----------
        self.x : str
            Input a string and remove utf-8 BOM if it exist

        Returns
        -------
        str
            The resulting utf-8 string without BOM.

        """
        return x.encode('utf-8').lstrip(b'\xef\xbb\xbf').decode('utf-8')
      
##########
    def links_of_pages(self, 
                       filename: str = "links_of_pages_registration",
                       savefile: bool = False) -> pd.DataFrame:
        """This function grabs all landing pages of movie registrations
        @return links_of_pages: pd.DataFrame
        """
        req = Request(url=self.url_reg, headers=self.headers) 
        with urlopen(req) as x: 
            html = x.read().decode('utf-8')
            
        bsObj = BeautifulSoup(html, 'html5lib')
        str_total_number_of_pages = bsObj.find(text=re.compile(u'共[0-9]*页'))
        total_number_of_pages = int(str_total_number_of_pages[1:-1])
        
        links_of_pages = [self.url_reg]
        for n in range(2, total_number_of_pages+1):
            links_of_pages.append(self.url_reg[:-6] + '_' + str(n) + '.shtml')
        
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])

        if savefile:
            self.save_records(links_of_pages, filename, backup=True)
            
        return links_of_pages

########## 
    def links_of_publications(self, 
                              links_of_pages: pd.DataFrame = 'default',
                              filename: str = "links_of_publications", 
                              savefile: bool = False) -> pd.DataFrame:
        """
        This functions grabs the links of registration publications

        Parameters
        ----------
        links_of_pages : pd.DataFrame, optional
            DESCRIPTION. The default is 'default', ['default'|'empty'|pd.DataFrame()]
        filename : str, optional
            DESCRIPTION. The default is "PubThreatricalRegistration_links_allpublishes".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_publications : TYPE
            DESCRIPTION.

        """
        if links_of_pages == 'default':
            links_of_pages = self.links_of_pages_latest
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        links_of_publications = []
        for _, page in links_of_pages.iterrows():
            req = Request(url=page['links_of_pages'], headers=self.headers) 
            with urlopen(req) as x: 
                html = x.read().decode('utf-8')   # site has problem decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find_all('a', class_="m2r_a"):
                links_of_publications += [[self.url_base + item.get("href"), str(item.text)[1:]]]
        if len(links_of_publications) != 0:
            links_of_publications = pd.DataFrame(links_of_publications)
            links_of_publications.columns = ['公示批次链接','名称缩减']
        else:
            links_of_publications = pd.DataFrame(columns = ['公示批次链接','名称缩减'])
           
        if savefile:
            self.save_records(links_of_publications, filename, backup=True)
            
        return links_of_publications
##########

    def links_of_new_publications(self, 
                                  filename: str = "links_of_publications",
                                  update_records: bool = False) -> pd.DataFrame:
        """
        This functions finds the links to new publications
        @param update_records: bool, whether to updated the saved records
        @return records_new: pd.DataFrame
        """       
           
        # Get latest links of publication from NRTA
        links_of_publications_latest = self.links_of_publications()
        
        # Check with existing links for new link(s) of publication(s)
        links_of_publications_new = links_of_publications_latest[
            ~links_of_publications_latest['公示批次链接'].isin(
                self.links_of_publications_existing['公示批次链接'])]

        if update_records:
            self.save_records(links_of_publications_latest, filename, backup=True)
            print(filename + '.json updated.')
        
        return links_of_publications_new

##########
    def links_of_registrations(self, 
                               links_of_publications: pd.DataFrame, 
                               filename: str = "links_of_registrations",
                               savefile: bool = False) -> pd.DataFrame:
        """
        This functions finds the links of publications give links of pages

        Parameters
        ----------
        links_of_publications : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "PubThreatricalRegistration_links_allregistrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        pd.DataFrame

        """
        links_of_registrations = []
        for _, publication in links_of_publications.iterrows():
            req = Request(url=publication['公示批次链接'], headers=self.headers) 
            with urlopen(req) as x:
                html = x.read()
                bsObj = BeautifulSoup(html, 'html5lib')
                tables = bsObj.find_all('table')
                tbs = []
                for table in tables:
                    tb = []
                    for tr in table.find_all("tr"):
                        row = []
                        if tr.find('a'):
                            row.append(self.url_base + tr.find('a').get('href'))
                        else:
                            row.append('备案详细页链接')
                        for td in tr.find_all("td"):
                            row.append(re.sub('[\n\s]*', '', td.text)) # clean spaces and breaks
                        tb.append(row)
                    tb = pd.DataFrame(tb[1:], columns=tb[0])
                    tbs.append(tb)
                links_of_registrations_per_publication = pd.concat([tbs[i] for i in range(len(tbs))], ignore_index=True)
                
                dt_publish = bsObj.find('span', class_='fl').text
                dt_publish = re.match('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-3][0-9]', dt_publish)[0]

                links_of_registrations_per_publication['公示日期']= dt_publish
                links_of_registrations_per_publication['公示批次链接'] = publication['公示批次链接']
                links_of_registrations_per_publication['公示批次名称'] = bsObj.find('title').text
        
            links_of_registrations.append(links_of_registrations_per_publication)
        
        if len(links_of_registrations) != 0:
            links_of_registrations = pd.concat([links_of_registrations[i] for i in range(len(links_of_registrations))], ignore_index=True)
        else:
            links_of_registrations = pd.DataFrame(columns = ['序号', '备案立项号', '片名', '备案单位', '编剧', '备案结果', '备案地', '公示日期', '公示批次链接',
       '公示批次名称'])
   
        
        if savefile:
            self.save_records(links_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')

        return links_of_registrations
 
##########
    def links_of_new_registrations(self, 
                                   filename: str = "links_of_registrations" ,
                                   comprehensive: bool = False,
                                   update_records: bool = False) -> pd.DataFrame:
        """
        This functions gets the links of new registrations not currently in record.

        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "PubThreatricalRegistration_links_allregistrations".
        comprehensive : bool, optional
            DESCRIPTION. The default is False. 
                         [True], will fetch page and publications links from scratch to construct records
                         [False], willrerun use differences from links_of_publications to fill in new records
        update_records : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        links_of_new_registrations : TYPE
            DESCRIPTION.

        """
        # Get latest links of publication from NRTA
        links_of_publications_latest = self.links_of_publications()
        links_of_registrations_latest = self.links_of_registrations(
            links_of_publications_latest)

        links_of_registrations_new = links_of_registrations_latest[
            ~links_of_registrations_latest['备案详细页链接'].isin(
                self.links_of_registrations_existing['备案详细页链接'])
            ]
             
        if update_records:
            self.save_records(links_of_registrations_latest , 
                              filename, backup=True)
            print(filename + '.json updated.')
            
        return links_of_registrations_new

##########
    def contents_of_registrations(self, 
                                  links_of_registrations: pd.DataFrame, 
                                  filename: str = "contents_of_registrations",
                                  savefile: bool = False) -> pd.DataFrame:

        """
        This functions grabs the contents of film registrations

        Parameters
        ----------
        links_of_registrations : pd.DataFrame
            DESCRIPTION.
        filename : str, optional
            DESCRIPTION. The default is "PubTheatricalRegistration_info_allregistrations".
        savefile : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        pd.DataFrame
            DESCRIPTION.

        """
        contents_of_registrations = []
        unprocessed_links = []
        for _, link in links_of_registrations.iterrows():
            self.driver.get(link['备案详细页链接'])
            print(link['片名'], '...')
            self.driver.implicitly_wait(2) # or use 5 seconds random.randint(2,5)
            html = self.driver.page_source
            bsObj_reg = BeautifulSoup(html, 'html.parser')
            tables = pd.read_html(str(bsObj_reg.find('form', id='form1')), index_col=0)
            if tables:
                table = tables[0].T
                table['公示日期'] = link['公示日期']
                table['公示批次名称'] = link['公示批次名称']
                table['备案详细页链接'] = link['备案详细页链接']
                table['公示批次链接'] = link['公示批次链接']
                contents_of_registrations.append(table)
            else:
                unprocessed_links.append[link]

        if len(contents_of_registrations) != 0:
            contents_of_registrations = pd.concat([contents_of_registrations[i] for i in range(len(contents_of_registrations))], ignore_index=True)
            contents_of_registrations['梗概'] = contents_of_registrations['梗概'].apply(lambda x: x.lstrip('梗概：'))
        else:
            contents_of_registrations = pd.DataFrame(columns = ['备案立项号', '片名', '备案单位', '编剧', '备案结果', '备案地', '梗概', '公示日期', '公示批次名称',
       '备案详细页链接', '公示批次链接'])
        
        if unprocessed_links:
            unprocessed_links = pd.concat([unprocessed_links[i] for i in range(len(unprocessed_links))], ignore_index=True)
            unprocessed_links.to_cvs(self.path_logs + 'unprocessed_records.csv', encoding='utf-8-sig', index=False)
            print('Some records remained unprocess, check logs/unprocessed_records.csv for more information.')
            
        if savefile:
            self.save_records(contents_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
                  
        return contents_of_registrations

##########
    def contents_of_new_registrations(self, 
        filename: str = "contents_of_registrations",
        save_update: bool = False) -> pd.DataFrame:
        """      
        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        save_update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        contents_of_registrations_new : TYPE
            DESCRIPTION.

        """

        # Get latest links of publication from NRTA
        links_of_publications_latest = self.links_of_publications()
        links_of_registrations_latest = self.links_of_registrations(
            links_of_publications_latest)
        
        links_of_registrations_new = links_of_registrations_latest[
            ~links_of_registrations_latest['备案详细页链接'].isin(
                self.contents_of_registrations_existing['备案详细页链接'])
            ]
        
        # Concat existing contents with new contents
        contents_of_registrations_new = self.contents_of_registrations(
            links_of_registrations_new)

        if save_update:        
        # Save Updated Records
            self.save_records(links_of_publications_latest, 
                              'links_of_publications')
            self.save_records(links_of_registrations_latest, 
                                  'links_of_registrations')       

            
            n_new_records = links_of_registrations_new.shape[0]
            print('Records from ' + str(n_new_records)
                  + ' publication(s) are added to links of registrations.')
            
        return  contents_of_registrations_new   
##########
    def contents_of_registrations_in_batch(self, 
        links_of_registrations: pd.DataFrame, 
        filename: str = "contents_of_registrations_in_batch",
        i: int = 0,
        batch_size: int = 5,
        ) -> pd.DataFrame:
        """
        WIP
        """
        while i < links_of_registrations.shape[0]:
            records = self.contents_of_registrations(
                links_of_registrations[i:i+batch_size])
            i += batch_size
            print(i, '--------------------')
            
            self.append_records(records, filename)
        
        records_accumulated = pd.read_csv(self.path_records + '//' + filename + '.csv')
        records_accumulated.drop_duplicates(inplace=True)
        return records_accumulated
        
##########
    def update_records(self, 
        fn_links_of_publications: str = "links_of_publications",
        fn_links_of_registrations: str = "links_of_registrations" ,
        fn_contents_of_registrations: str = "contents_of_registrations",
        how:str ='quick',
        save_update: bool = False
        ) -> pd.DataFrame:
        """
        This functions updates the records to latest.

        Parameters
        ----------
        fn_links_of_publications : str, optional
            DESCRIPTION. The default is "links_of_publications".
        fn_links_of_registrations : str, optional
            DESCRIPTION. The default is "links_of_registrations".
        fn_contents_of_registrations : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        save_update : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        contents_of_registrations_updated : TYPE
            DESCRIPTION.

        """
        # Compares existing links of registrations in Content df with 
        # latest links in links of registrations df
        if how == 'comprehensive':
            # Get latest links of publication from NRTA
            links_of_publications_latest = self.links_of_publications()
            links_of_registrations_latest = self.links_of_registrations(
                links_of_publications_latest)
            
            links_of_registrations_new = links_of_registrations_latest[
                ~links_of_registrations_latest['备案详细页链接'].isin(
                    self.contents_of_registrations_existing['备案详细页链接'])
                ]
        
        # Compares existing links of publications in Content df with 
        # latest links in links of publications df
        if how == 'quick':
            
            links_of_publications_latest = self.links_of_publications()
            links_of_publications_new = links_of_publications_latest[
                ~links_of_publications_latest['公示批次链接'].isin(
                    self.contents_of_registrations_existing['公示批次链接'])
                ]
            links_of_registrations_new = self.links_of_registrations(
                links_of_publications_new)
         
        # Concat existing contents with new contents
        contents_of_registrations_new = self.contents_of_registrations(
            links_of_registrations_new)
        
        contents_of_registrations_latest = pd.concat(
            [self.contents_of_registrations_existing, contents_of_registrations_new],
            ignore_index=True)
        
        contents_of_registrations_latest.drop_duplicates(inplace=True)
        
        contents_of_registrations_latest = contents_of_registrations_latest.sort_values(
            '公示日期', ascending=True).reset_index(drop=True)
        
        contents_of_registrations_latest = contents_of_registrations_latest.sort_values(
            '公示日期', ascending=False)
            
        
        if save_update:        
        # Save Updated Records
            self.save_records(links_of_publications_latest, 
                              fn_links_of_publications)
            if 'links_of_registrations_latest' in locals():
                self.save_records(links_of_registrations_latest, 
                                  fn_links_of_registrations)       
            self.save_records(contents_of_registrations_latest, 
                              fn_contents_of_registrations)
            
            n_new_records = (contents_of_registrations_latest.shape[0] -
                self.contents_of_registrations_existing.shape[0])
            print('Records from ' + str(n_new_records)
                  + ' publication(s) are added to contents of registrations.')
            
        return  contents_of_registrations_latest


##########    
    def Refined_Records(self, 
        fn_raw: str = "contents_of_registrations",
        fn_refined: str = 'contents_of_registrations_refined',
        update_first: bool = True,
        save_refined: bool = False
        ) -> pd.DataFrame:
        """
        This functions refines and parsers raw registration data to features.

        Parameters
        ----------
        fn_raw : str, optional
            DESCRIPTION. The default is "contents_of_registrations".
        fn_refined : str, optional
            DESCRIPTION. The default is 'contents_of_registrations_refined'.
        update_first : bool, optional
            DESCRIPTION. The default is True.
        save_refined : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        contents_of_registrations_refined : TYPE
            DESCRIPTION.

        """
        if update_first:
            contents_of_registrations_raw = self.update_records()
        
        elif os.path.isfile(self.path_records + '//' + fn_raw + '.json'):
            contents_of_registrations_raw = pd.read_json(
                self.path_records + '//' + fn_raw + '.json')
        else:
            contents_of_registrations_raw = self.contents_of_registrations(pd.DataFrame())

        #======== REFININIG RECORDS
        contents_of_registrations_refined = contents_of_registrations_raw.copy()
        
        # Convert to datetiime
        contents_of_registrations_refined['公示日期'] = pd.to_datetime(contents_of_registrations_refined['公示日期'])
        
        # Extract Publish Year
        contents_of_registrations_refined['公示年'] = contents_of_registrations_refined['公示日期'].apply(lambda x: x.year)

        # Corrrect Publication Title Errors
        contents_of_registrations_refined['公示批次名称'] = contents_of_registrations_raw.agg(
            self.parser.correct_publication_title_errors, axis=1)
               
        # Drop duplicates after corrections
        contents_of_registrations_refined.drop_duplicates(inplace=True)

        # Extract parsed Pubtitle
        contents_of_registrations_refined['公示批次起始'] = contents_of_registrations_refined['公示批次名称'].agg(self.parser.PubTitle)
        contents_of_registrations_refined['公示批次起始'] = contents_of_registrations_refined['公示批次起始'].apply(lambda x: tuple(x))
        
        # Parse Film Type
        contents_of_registrations_refined['类型'] = contents_of_registrations_raw['备案立项号'].agg(
            self.parser.RegType)
        
        # Extract Reg Submit Year
        contents_of_registrations_refined['备案申请年份'] = contents_of_registrations_raw['备案立项号'].agg(
            self.parser.RegSubmitYear)
        
        # Extract Reg Sequence Number
        contents_of_registrations_refined['备案立项年度顺序号'] = contents_of_registrations_raw['备案立项号'].agg(
            self.parser.RegSequenceNo)
           
        # Correct pre_2011 备案立项年度顺序号 errors
        contents_of_registrations_refined['备案立项年度顺序号'] = contents_of_registrations_refined.agg(
            self.parser.correct_pre_2011_error, axis=1)
        
        # Extract PubIssue Date Range
        contents_of_registrations_refined['公示覆盖期间'] = self.parser.DateRange(contents_of_registrations_raw['公示批次名称'])
        
    
        # Calculate Number of days covered in Issue
        contents_of_registrations_refined['公示覆盖天数'] = contents_of_registrations_refined['公示覆盖期间'].apply(lambda x: len(x))
        
        # Convert dtypes
        contents_of_registrations_refined = contents_of_registrations_refined.convert_dtypes()
        
        # Return
        return contents_of_registrations_refined
##########

##########==========##########==========##########==========##########==========
class Parser_Registration(object):
    
##########
    def __init__(self):
        super(Parser_Registration, self).__init__()
            
##########           
    def correct_publication_title_errors(self, df_row: pd.DataFrame) -> str:
        """
        This functions corrects known publication title typos, can be used with pandas apply and agg along axis=1

        Parameters
        ----------
        pubtitle : pd.DataFrame
            for use with the apply or agg fucntion, along axis=1
        publink : str
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        pubtitle, publink = df_row['公示批次名称'], df_row['公示批次链接']
        publication_title_errors = {
         'http://dy.chinasarft.gov.cn/shanty.deploy/blueprint.nsp?id=014d1d2c7258636b402881a74cc1e374&templateId=0129f8148f650065402881cd29f7df33':
         '国家新闻出版广电总局电影局关于2015年04月（上旬）全国电影剧本（梗概）备案、立项公示的通知',
         
         'http://dy.chinasarft.gov.cn/shanty.deploy/blueprint.nsp?id=013459855d1d1413402881a6344513a3&templateId=0129f8148f650065402881cd29f7df33':
         '广电总局电影局关于2011年11月（下旬）全国电影剧本（梗概）备案、立项公示的通知',
         
         'http://dy.chinasarft.gov.cn/shanty.deploy/blueprint.nsp?id=01387536929c725a402881a737c5ff2c&templateId=0129f8148f650065402881cd29f7df33':
         '广电总局电影局关于2012年06月（下旬）全国电影剧本（梗概）备案、立项公示的通知'}
        
        if publink in publication_title_errors:
            pubtitle = publication_title_errors[publink]
            
        return pubtitle
##########
    def correct_pre_2011_error(self, df_row: pd.DataFrame) -> str:
        """
        This functions corrects pre 2011 errors, for use with agg/apply along axis=1

        Parameters
        ----------
        df_row : pd.DataFrame
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
        pre_2011_sequence_errors = {
        'http://dy.chinasarft.gov.cn/shanty.deploy/blueprint.nsp?id=0132282c2ff6113b402881a732237dea&templateId=012a2e051030004740284c812a2d62df':
        966,
        
        'http://dy.chinasarft.gov.cn/shanty.deploy/blueprint.nsp?id=0132282c2fd21139402881a732237dea&templateId=012a2e051030004740284c812a2d62df':
        38
        }
            
        publink, sequence_no = df_row['备案详细页链接'], df_row['备案立项年度顺序号']
        if publink in pre_2011_sequence_errors:
            sequence_no = pre_2011_sequence_errors[publink]
            
        return sequence_no    
        
            
##########     
    def PubDate(self, regpubdate: str) -> datetime:
        """
        This function converts raw Publication Date to Datetime Formats

        Parameters
        ----------
        regpubdate : str
            DESCRIPTION.

        Returns
        -------
        datetime
            DESCRIPTION.

        """
        #sample = '2019-03-11 17:21'
        dt = datetime.datetime.strptime(regpubdate, "%Y-%m-%d %H:%M")
        return dt

    def IssueDate(self, string_issuedate):
#        sample = '2019-03-11'
        dt = datetime.datetime.strptime(string_issuedate, "%Y-%m-%d")
        return dt

#########   
    def RegType(self, regid: str) -> str:
        """
        This functions extracts the movie type from the RegID,
        to be used in pandas agg or apply with series or dataframes

        Parameters
        ----------
        regid : pd.Series
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """       
        idtype_2_dytype = {'影剧备字': '故事片',
                          '影纪备字': '纪录片',
                          '影特备字': '特种片',
                          '影科备字': '科教片',
                          '影动备字': '动画片',
                          '影重备字': '重大历史题材片',
                          '影复协字': '协拍片',
                          '影立协字': '协拍片',
                          '影协立字': '协拍片',
                          '影协证字': '协拍片',
                          '影合立字': '合拍片',
                          '影立合字': '合拍片',
                          '影合证字': '合拍片'
                          }
        reg_type = np.nan
        for key, value in idtype_2_dytype.items():
            if key in str(regid):
                reg_type = value
        
        return reg_type

########
    def RegSubmitYear(self, regid: str) -> str:
        """
        This functions extracts the submit year from the RegId,

        Parameters
        ----------
        regid : str
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """       
        # 从备案号提取 年份
        pat = '[\[【（(〔][0-9][0-9][0-9][0-9][〕)）】\]]'
        pat = re.compile(pat)
        reg_submit_year = pat.search(str(regid))

        if reg_submit_year:
            reg_submit_year = reg_submit_year.group()
            reg_submit_year = reg_submit_year.lstrip('[\[【（(〔]').rstrip('[〕)）】\]]')
            reg_submit_year = int(reg_submit_year)
        else:
            reg_submit_year = np.nan
        
        return reg_submit_year

##########    
    def RegSequenceNo(self, regid: str) -> int:
        """
        This function extracts the reg sequence number from RegId.

        Parameters
        ----------
        regid : str
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """
         # 从备案号提取 备案顺序号
        pat = u'第.*?号|][0-9].*|）[0-9].*号'
        pat = re.compile(pat)
        reg_sequence_no = pat.search(str(regid))
        
        if reg_sequence_no:
            reg_sequence_no = reg_sequence_no.group()
            reg_sequence_no = reg_sequence_no.lstrip('[第\]）]').rstrip('[号]')
            reg_sequence_no = int(reg_sequence_no)
        else:
            reg_sequence_no = np.nan            
        return reg_sequence_no
 
 ##########
    def PubTitle(self, pubtitle: str) -> tuple:
        """
        This functions breaks the putitle down to start and end months

        Parameters
        ----------
        pubtitle : strss
            DESCRIPTION.

        Returns
        -------
        list[yr:str, start_m:str, start_mq: str, end_m: str, end_mq: str]
            DESCRIPTION.

        """
            
        pat = re.compile(u'关于.*全国')
        pt = pat.search(pubtitle)
        if pt:
            pt = pt.group()
            pt = pt.lstrip('关于').rstrip('全国')
        else:
            pt = np.nan
        #2016年09月（下旬）10月（上旬）
        #2020年01月下、02月
        #2019年08月（上旬）
        #2017年09月（下旬）、10月（上旬）
        #2017年09月（中旬）
        #2015年09月（下旬）、10月（上旬）
        #2013年04月（下旬）、05月（上旬）
        #2012年01月
        #2011年12月（下旬）   
        #2020年01月（上旬、中旬）
        if pt:
            yr, m = pt.split('年')[0], pt.split('年')[1]
            m  = re.split('[）、]', m)
            m = [n for n in m if n != '']
            
            start_m = m[0].split('月')[0]
            if u'上' in m[0]:
                start_mq = u'上旬'
            elif u'中' in m[0]:
                start_mq = u'中旬'
            elif u'下' in m[0]:
                start_mq = u'下旬'
            else:
                start_mq = '整月'
            
            end_m = m[-1].split('月')[0]
            if u'月' not in m[-1]:
                end_m = start_m
            if u'上' in m[-1]:
                end_mq = u'上旬'
            elif u'中' in m[-1]:
                end_mq = u'中旬'
            elif u'下' in m[-1]:
                end_mq = u'下旬'
            else:
                end_mq = '整月'
               
        return [yr, start_m, start_mq, end_m, end_mq]
    
##########
    def DateRange(self, pubtitle: pd.Series)-> pd.DatetimeIndex:
        """
        This Function extracts date range from Pubtitle, required pubtitle parser.
    
        Parameters
        ----------
        pubtitle : pd.Series
            DESCRIPTION.
    
        Returns
        -------
        pd.DatetimeIndex
            DESCRIPTION.
    
        """
        pubtitle_unique = pubtitle.drop_duplicates().rename('本批次周期')
        pubtitle_unique = pubtitle_unique.agg(self.PubTitle)
        pubtitle_unique = pubtitle_unique.to_frame()
        pubtitle_unique['上一批次周期'] = pubtitle_unique['本批次周期'].shift(-1)
        pubtitle_unique['下一批次周期'] = pubtitle_unique['本批次周期'].shift(1)
        pubtitle_unique.fillna(value='['', '', '', '']', inplace=True)
        
        def gen_dr(df_row: pd.DataFrame) -> pd.date_range:
            start_yr = int(df_row['本批次周期'][0])
            start_mon = int(df_row['本批次周期'][1])
            
            # 本批次 起始日期
            if  df_row['本批次周期'][2] == u'上旬':
                start_d = 1
            elif df_row['本批次周期'][2] == u'中旬':
                start_d = 11
            elif df_row['本批次周期'][2] == u'整月':
                start_d = 1
            else:
                start_d = 16
                if df_row['上一批次周期'][4] == '中旬':
                    start_d = 21
            start_date = date(start_yr, start_mon, start_d)
            
            # 本批次 结束日期
            end_yr = int(df_row['本批次周期'][0])
            end_mon = int(df_row['本批次周期'][3])
            if df_row['本批次周期'][4] == u'中旬':
                end_d = 20
            elif df_row['本批次周期'][4] == u'下旬' or df_row['本批次周期'][4] == u'整月':
                end_d = (date(end_yr, end_mon, 1) + MonthEnd(1)).day
            else:
                end_d = 15
                if df_row['下一批次周期'][2] == '中旬':
                    end_d = 10
            end_date = date(end_yr, end_mon, end_d)
            dt_range = pd.date_range(start_date, end_date)
            return  dt_range
        
        dt_range = pubtitle_unique.agg(gen_dr, axis=1) #Series
        dt_range.rename('公示覆盖期间', inplace=True)
        
        df = pd.concat([pubtitle, dt_range], axis=1)
        df['公示覆盖期间'].fillna(method='ffill', inplace=True)
        
        return df['公示覆盖期间']        
##########==========##########==========##########==========##########==========
class Estimate_Registration(object):
##########
    def __init__(self):
        super(Estimate_Registration, self).__init__()


##########        
    def complete_dt(self,
                    df: pd.DataFrame, 
                    comprehensive: bool = False, 
                    plot: bool = False) -> pd.DataFrame:
        """
        This function estimates the registration completion time.

        Parameters
        ----------
        df : pd.DataFrame
            df with columns  ['公示日期', '备案立项年度顺序号']
        comprehensive : bool, optional
            DESCRIPTION. The default is False.
        plot : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        pd.DataFrame
            DESCRIPTION.

        """        
        # narrow down 
        #df_tmp = df.groupby('公示日期')['备案立项年度顺序号'].max().reset_index()
        if df.shape[0] > 5:
            #df_tmp = df.groupby('公示日期')['备案立项年度顺序号'].quantile(0.65).reset_index()
            df_tmp = df.groupby('公示日期')['备案立项年度顺序号'].describe(percentiles=[0.65])['65%'].apply(lambda x: int(x))
            df_tmp = df_tmp.rename('备案立项年度顺序号').reset_index()
            dt_min = df_tmp.loc[:,'公示日期'].min()
            df_tmp['自最早天数'] = df_tmp.loc[:,'公示日期'].apply(lambda x: (x-dt_min).days)
            exclude_beyond = df_tmp.loc[:,'备案立项年度顺序号'].quantile(0.9)
            cut_off_day = df_tmp.loc[df_tmp['备案立项年度顺序号'] >= exclude_beyond, '自最早天数'].min()
            df_tmp = df_tmp.loc[df_tmp['自最早天数'] < cut_off_day]
        else:
            df_tmp = df[['公示日期', '备案立项年度顺序号']]
            dt_min = df_tmp['公示日期'].min()
            df_tmp.loc[:,'自最早天数'] = df_tmp.loc[:,'公示日期'].apply(lambda x: (x-dt_min).days)
            
        # Fitting, Poly with 3 degrees
        df_tmp = df_tmp.dropna()
        X_train = df_tmp.loc[:,'备案立项年度顺序号'].tolist()
        X_train = np.array(X_train).reshape(-1, 1)
        y_train = df_tmp.loc[:,'自最早天数']
        model = model = make_pipeline(PolynomialFeatures(1), Ridge())
        fitted = model.fit(X_train, y_train)
        
        X_pred = np.array(range(1, int(round(df.loc[:,'备案立项年度顺序号'].max()+1)))).reshape(-1, 1)
        y_pred = fitted.predict(X_pred)
        y_pred = np.array([0 if y < 0 else int(round(y)) for y in y_pred])
        x2y = dict(np.array([np.squeeze(X_pred), y_pred], dtype='int').T)
        
        if plot:
            plt.plot(X_pred, y_pred)
            plt.plot(X_train, y_train)      
        
        df['自最早天数估计'] = df.loc[:,'备案立项年度顺序号'].apply(lambda x: x2y[x])
        df['备案公示日期预测'] = df.loc[:, '自最早天数估计'].apply(lambda x: dt_min + timedelta(days=x))
        df['备案通过日偏差'] = df.loc[:, '公示日期'] - df.loc[:, '备案公示日期预测'] 
        df.loc[:, '备案通过日偏差'] =  df.loc[:, '备案通过日偏差'].apply(lambda x: x.days)
           
        if comprehensive:
            return df
        return df[['备案立项年度顺序号', '公示日期', '备案公示日期预测', '备案通过日偏差']]