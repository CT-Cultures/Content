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

import datetime
from pathlib import Path
import os

######################################################################
class Registration(object):
 
    def __init__(self):
        """
        """
        super(Registration, self).__init__()
        
        # 中国电影政务平台网址
        self.url_base = "http://dy.chinasarft.gov.cn"
        
        # 电影备案立项网址
        self.url_reg = "http://dy.chinasarft.gov.cn/html/www/catalog/0129dffcccb1015d402881cd29de91ec.html"
        
        # folder for saving records, relative
        self.path_records = 'records'
        
        # links of pages from web
        self.links_of_pages = self.links_of_pages()
        
        # Call Parser Class
        self.parser = Parser_Registration()
        
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
        path_file = self.path_records + '//' + filename + '.csv'
        path_file_bk = self.path_records + '//backup//' + filename + appendix_dt + '.csv'
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        records.to_csv(path_file, encoding='utf-8-sig', index=False)
        print('file saved to: ' + filename + '.csv')

        
##########
    def links_of_pages(self) -> pd.DataFrame:
        """This function grabs all landing pages of movie registrations
        @return links_of_pages: pd.DataFrame
        """
        with urlopen(self.url_reg) as x: 
            html = x.read().decode('utf-8')
        links_of_pages = []
        bsObj = BeautifulSoup(html, 'html5lib')
        for item in bsObj.find_all(href=re.compile("pageIndex")):
           links_of_pages += (self.url_base + item.get("href"),)
        links_of_pages = links_of_pages[0:-2]# 删除最后两个链接：下一页与最后一页
        
        if len(links_of_pages) != 0:
            links_of_pages = pd.DataFrame(links_of_pages)
            links_of_pages.columns = ['links_of_pages']
        else:
            links_of_pages = pd.DataFrame(columns =['links_of_pages'])
            
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
            links_of_pages = self.links_of_pages
        elif links_of_pages == 'empty':
            links_of_pages = pd.DataFrame()
        links_of_publications = []
        for _, page in links_of_pages.iterrows():
            with urlopen(page['links_of_pages']) as x: 
                html = x.read()   # site has probelm decoding
            bsObj = BeautifulSoup(html, 'html5lib')
            for item in bsObj.find_all(href=re.compile("blueprint.nsp?")):
                links_of_publications += [[self.url_base + item.get("href"), str(item.next_element)]]
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
       
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', encoding='utf-8-sig')
        else:
            records_existing = self.links_of_publications(links_of_pages = 'empty')
            
        # 网上获取最新
        records_latest = self.links_of_publications()
        records_new = records_latest[~records_latest['公示批次链接'].isin(records_existing['公示批次链接'])]

        if update_records:
            self.save_records(records_latest, filename, backup=True)
            print(filename + '.csv updated.')
        
        return records_new

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
        url_part_blueprint = '/shanty.deploy/blueprint.nsp?'
        templateId = 'templateId=012a2e051030004740284c812a2d62df'     
        pattern_id = re.compile("id=.*?&")  # 定义查找id的规律 
        for _, publication in links_of_publications.iterrows():
            with urlopen(publication['公示批次链接']) as x:
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
                        print(str(len(links_of_registrations)), ": ")
                        print("str(item): " + str(item))
                        print("str_item: " + str_item)
                    url_link_reg = self.url_base + url_part_blueprint + str_id + templateId
#                    print(url_link_reg)
                    links_of_registrations += [[dt_publish, title_publish, url_link_reg, publication['公示批次链接']]]
        if len(links_of_registrations) != 0:
            links_of_registrations = pd.DataFrame(links_of_registrations)
            links_of_registrations.columns = ['公示日期', '公示批次名称', '制作表链接', '公示批次链接']
        else:
            links_of_registrations = pd.DataFrame(columns = ['公示日期', '公示批次名称', '制作表链接', '公示批次链接'])
        
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
        # Import Existing Records
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', encoding='utf-8-sig')
        else:
            records_existing = self.links_of_registrations(links_of_publications = pd.DataFrame())            
            
        if comprehensive:
            links_of_publications = self.links_of_publications()
            records_latest = self.links_of_registrations(links_of_publications)
            records_new = records_latest[~records_latest['备案详细页链接'].isin(records_existing['备案详细页链接'])]
        else:
            links_of_new_publications = self.links_of_new_publications(update_records=update_records)
            records_new = self.links_of_registrations(links_of_new_publications)
            records_latest = pd.concat([records_new, records_existing], axis=0, ignore_index=True, sort=False)
            records_latest = records_latest.drop_duplicates(keep='first')
             
        if update_records:
            self.save_records(records_latest , filename, backup=True)
            print(filename + '.csv updated.')
            
        return records_new

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
        for _, link in links_of_registrations.iterrows():
            with urlopen(link['制作表链接']) as x:
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
            tb_row_third.append(link['公示批次链接'])
#            print(tb_row_third)
            info_reg = tb_row_second + tb_row_third
#            print(tb_info_reg)
            contents_of_registrations += [info_reg]
#        print("Total number of " + str(len(info_allregistrations)-1) + " registration info scrapped from web.")
        if len(contents_of_registrations) != 0:
            contents_of_registrations = pd.DataFrame(contents_of_registrations)
            contents_of_registrations.columns = ['备案立项号','片名','备案单位','编剧','备案结果','备案地',
                                                 '梗概','公示日期','公示批次名称','制作表链接', '公示批次链接']
        else:
            contents_of_registrations = pd.DataFrame(columns=
                                         ['备案立项号','片名','备案单位','编剧','备案结果','备案地',
                                          '梗概','公示日期','公示批次名称', '制作表链接', '公示批次链接'])

        if savefile:
            self.save_records(contents_of_registrations, filename, backup=True)
            print(filename + '.csv updated.')
                  
        return contents_of_registrations

##########
    def contents_of_new_registrations(self, 
                                      filename: str = "contents_of_registrations",
                                      comprehensive: bool = False,
                                      update_records: bool = False) -> pd.DataFrame:
        """
        This functions gets the contents of new registrations

        Parameters
        ----------
        filename : str, optional
            DESCRIPTION. The default is "PubTheatricalRegistration_info_allregistrations".
        update_records : bool, optional
            DESCRIPTION. The default is False. If True, will update:
                            links_of_new_publications,
                            links_of_new_registrations,
                            contents_of_new_registrations

        Returnss
        -------
        DataFrame
            DESCRIPTION.

        """
        # Import Existing Records
        if os.path.isfile(self.path_records + '//' + filename + '.csv'):
            records_existing = pd.read_csv(self.path_records + '//' + filename + '.csv', encoding='utf-8-sig')
        else:
            records_existing = self.contents_of_registrations(links_of_registrations = pd.DataFrame())
        
        if comprehensive:
            links_of_publications = self.links_of_publications()
            links_of_registrations = self.links_of_registrations(links_of_publications)
            records_latest = self.contents_of_registrations(links_of_registrations)
            records_new = records_latest[~records_latest['备案立项号'].isin(records_existing['备案立项号'])]
        else:
            links_of_new_registrations = self.links_of_new_registrations()
            records_new = self.contents_of_registrations(links_of_new_registrations)
            records_latest = pd.concat([records_new, records_existing], axis=0, ignore_index=True, sort=False)
            records_latest = records_latest.drop_duplicates(keep='first').reindex()
            
        if update_records:
              self.save_records(records_latest, filename, backup=True)
              print("Contents of Registrations updated: ", + len(links_of_new_registrations ), " record(s).")

        return records_new
    
##########
    def update_records(self, 
                       fn_links_of_publications: str = "links_of_publications",
                       fn_links_of_registrations: str = "links_of_registrations" ,
                       fn_contents_of_registrations: str = "contents_of_registrations",
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
        
        # Import Existing Records:
        if os.path.isfile(self.path_records + '//' + fn_links_of_publications + '.csv'):
            links_of_publications = pd.read_csv(self.path_records + '//' + fn_links_of_publications + '.csv', encoding='utf-8-sig')
        else:
            links_of_publications = self.links_of_publications('empty')
        
        if os.path.isfile(self.path_records + '//' + fn_links_of_registrations + '.csv'):
            links_of_registrations = pd.read_csv(self.path_records + '//' + fn_links_of_registrations + '.csv', encoding='utf-8-sig')
        else:
            links_of_registrations = self.links_of_registrations(links_of_publications=pd.DataFrame())
            
        if os.path.isfile(self.path_records + '//' + fn_contents_of_registrations + '.csv'):
            contents_of_registrations = pd.read_csv(self.path_records + '//' + fn_contents_of_registrations + '.csv', encoding='utf-8-sig')
        else:
            contents_of_registrations = self.contents_of_registrations(links_of_registrations = pd.DataFrame())
        
        links_of_publications_latest = self.links_of_publications()

        # Find Records to update
        lp_latestest_not_in_lp_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(links_of_publications['公示批次链接'])]
        lp_old_not_in_lp_latest = links_of_publications[~links_of_publications['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]
        
        lp_latest_not_in_lr_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(links_of_registrations['公示批次链接'])]
        lr_old_not_in_lp_latest = links_of_registrations[~links_of_registrations['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]
        
        lp_latest_not_in_cr_old = links_of_publications_latest[~links_of_publications_latest['公示批次链接'].isin(contents_of_registrations['公示批次链接'])]
        cr_old_not_in_lp_latest = contents_of_registrations[~contents_of_registrations['公示批次链接'].isin(links_of_publications_latest['公示批次链接'])]
        
        lr_old_not_in_cr_old = links_of_registrations[~links_of_registrations['制作表链接'].isin(contents_of_registrations['制作表链接'])]
        cr_old_not_in_lr_old = contents_of_registrations[~contents_of_registrations['制作表链接'].isin(links_of_registrations['制作表链接'])]
        
        links_of_publications_to_update = pd.concat([   lp_latestest_not_in_lp_old['公示批次链接'],
                                                        lp_old_not_in_lp_latest['公示批次链接'],
                                                        lp_latest_not_in_lr_old['公示批次链接'],
                                                        lr_old_not_in_lp_latest['公示批次链接'],
                                                        lp_latest_not_in_cr_old['公示批次链接'],
                                                        cr_old_not_in_lp_latest['公示批次链接'],
                                                        lr_old_not_in_cr_old['公示批次链接'],
                                                        cr_old_not_in_lr_old['公示批次链接']
                                                    ], axis=0, ignore_index=True)
        
        links_of_publications_to_update.drop_duplicates(inplace=True)
        links_of_publications_to_update = links_of_publications_to_update.reset_index()

        if links_of_publications_to_update.shape[0] != 0:
            # Update corresponding records.      
            links_of_registrations_to_update = self.links_of_registrations(links_of_publications_to_update)              
            contents_of_registrations_to_update = self.contents_of_registrations(links_of_registrations_to_update)
    
            
            # Combine New Records with Existing Records and Remove Duplicates
            links_of_registrations_updated = pd.concat([links_of_registrations,
                                                        links_of_registrations_to_update],
                                                       axis=0, ignore_index=True)
            links_of_registrations_updated.drop_duplicates(subset='制作表链接', inplace=True)
            links_of_registrations.sort_values(by=['公示日期','制作表链接'], ascending=False, inplace=True)
            links_of_registrations.reset_index(drop=True, inplace=True)
            
            contents_of_registrations_updated = pd.concat([contents_of_registrations,
                                                           contents_of_registrations_to_update],
                                                          axis=0, ignore_index=True)        
            contents_of_registrations_updated.drop_duplicates(subset=['制作表链接','公示批次链接'], inplace=True)
            contents_of_registrations_updated.sort_values(by=['公示日期','制作表链接'], ascending=False, inplace=True)
            contents_of_registrations_updated.reset_index(drop=True, inplace=True)
        else:
            links_of_publications_latest = links_of_publications
            links_of_registrations_updated = links_of_registrations
            contents_of_registrations_updated = contents_of_registrations
            contents_of_registrations_updated.sort_values(by=['公示日期','制作表链接'], ascending=False, inplace=True)
            contents_of_registrations_updated.reset_index(drop=True, inplace=True)
        
        if save_update:        
        # Save Updated Records
            self.save_records(links_of_publications_latest, fn_links_of_publications)
            self.save_records(links_of_registrations_updated, fn_links_of_registrations)       
            self.save_records(contents_of_registrations_updated, fn_contents_of_registrations)
            print('Records from ' + str(len(links_of_publications_to_update)) + 'publication(s) are added to contents of registrations.')
            
        return contents_of_registrations_updated


##########    
    def Refined_Records(self, 
                             fn_raw: str = "contents_of_registrations",
                             fn_refined: str = 'contents_of_registrations_refined',
                             update_first: bool = True,
                             save_refined: bool = False
                             ) -> pd.DataFrame:
        if update_first:
            contents_of_registrations_raw = self.update_records()
        
        elif os.path.isfile(self.path_records + '//' + fn_raw + '.csv'):
            contents_of_registrations_raw = pd.read_csv(self.path_records + '//' + filename + '.csv', encoding='utf-8-sig')
        else:
            contents_of_registrations_raw = self.contents_of_registrations(pd.DataFrame())
            

        return contents_of_registrations_refined
            
        
##########

##########==========##########==========##########==========##########==========
class Parser_Registration(object):
    
##########
    def __init__(self):
        super(Parser_Registration, self).__init__()
            
##########           
    def correct_publication_title_errors(self, pubtitle: str, publink: str) -> str:
        """
        This functions corrects known publication title typos, can be used with pandas apply.

        Parameters
        ----------
        pubtitle : str
            DESCRIPTION.
        publink : str
            DESCRIPTION.

        Returns
        -------
        str
            DESCRIPTION.

        """

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

    def PubTitle(self, string_regpubtitle):
#        sample = '国家电影局关于2019年02月（下旬）全国电影剧本（梗概）备案、立项公示的通知'
#        sample2 = '国家电影局关于2019年02月（中旬）全国电影剧本（梗概）备案、立项公示的通知'
#        sample3 = '国家电影局关于2019年01月（下旬）、02月（上旬）全国电影剧本（梗概）备案、立项公示的通知'
#        sample4 = '国家新闻出版广电总局电影局关于2016年09月（下旬）10月（上旬）全国电影剧本（梗概）备案、立项公示的通知'
#        sample5 = '广电总局电影局关于2011年10月(上旬)全国电影剧本（梗概）备案、立项公示的通知'
        sample6 = '广电总局电影局关于2011年11月(上旬)全国电影剧本（梗概）备案、立项公示的通知'
        sample7 = '广电总局电影局关于2011年09月(下旬)全国电影剧本（梗概）备案、立项公示的通知'
        sample8 = '广电总局电影局关于2011年09月（上旬）全国电影剧本（梗概）备案、立项公示的通知'
        sample9 = '广电总局电影局关于2014年09月下旬全国电影剧本（梗概）备案、立项公示的通知'

        pattern_year = re.compile(u"关于[0-9][0-9][0-9][0-9]年")
        pattern_month = re.compile(u"年.*?月")
        pattern_month_additional = re.compile(u"、[0-9][0-9]月")
        pattern_month_additional2 = re.compile(u"）[0-9][0-9]月")
        pattern_partofmonth = re.compile(u"（.*?旬）")
        pattern_partofmonth_alt1 = re.compile(u"月(.*?旬)")
        pattern_partofmonth_alt2 = re.compile(u"月.*?旬")

        year = pattern_year.search(string_regpubtitle)
        if year:
            year = year.group().lstrip('关于').rstrip('年')
        else:
            year = "没有年"

        month = pattern_month.search(string_regpubtitle)
        if month:
            month = month.group().lstrip('年').rstrip('月')
            month_add = pattern_month_additional.search(string_regpubtitle)
            month_add2 = pattern_month_additional2.search(string_regpubtitle)
            if month_add:
                month_add = month_add.group().lstrip(u'、').rstrip('月')
                month = month + '、' + month_add
            if month_add2:
                month_add = month_add2.group().lstrip(u'）').rstrip('月')
                month = month + '、' + month_add
        else:
            month = "没有月"

        partofmonth = pattern_partofmonth.findall(string_regpubtitle)
        partofmonth_alt1 = pattern_partofmonth_alt1.findall(string_regpubtitle)
        partofmonth_alt2 = pattern_partofmonth_alt2.findall(string_regpubtitle)
        if partofmonth:
            if len(partofmonth) == 1:
                partofmonth = partofmonth[0].lstrip('（').rstrip('）')
            elif len(partofmonth) == 2:
                part1 = partofmonth[0].lstrip('（').rstrip('）')
                part2 = partofmonth[1].lstrip('（').rstrip('）')
                partofmonth = part1 + '、' + part2
        elif partofmonth_alt1:
            if len(partofmonth_alt1) == 1:
                partofmonth = partofmonth_alt1[0].lstrip('月(').rstrip(')')
            elif len(partofmonth_alt1) == 2:
                part1 = partofmonth_alt1[0].lstrip('月(').rstrip(')')
                part2 = partofmonth_alt1[1].lstrip('月(').rstrip(')')
                partofmonth = part1 + '、' + part2
        elif partofmonth_alt2:
            if len(partofmonth_alt2) == 1:
                partofmonth = partofmonth_alt2[0].lstrip('月(').rstrip(')')
            elif len(partofmonth_alt2) == 2:
                part1 = partofmonth_alt2[0].lstrip('月(').rstrip(')')
                part2 = partofmonth_alt2[1].lstrip('月(').rstrip(')')
                partofmonth = part1 + '、' + part2
        else:
            partofmonth = "没有旬"
        return [year, month, partofmonth]

    def RegID(self, string_regid):
#        sample1 = u'影剧备字[2009]720'
#        sample2 = u'影剧备字[2011]第1584号'
#        sample3 = u'待定'
#        sample4 = u'影立合字（2013）49号'
#        sample5 = u'影立合字【2012】第07号'
        RegNumber_parsed = []
        # 备案立项号 Type：电影片/记录片/合拍片/特种片/科教片
        pattern_type_regular = re.compile('影剧备字')
        pattern_type_documentary = re.compile('影纪备字')
        pattern_type_special = re.compile('影特备字')
        pattern_type_science = re.compile('影科备字')
        pattern_type_animation = re.compile('影动备字')
        pattern_type_significance = re.compile('影重备字')
        pattern_type_supporting = re.compile('影复协字')
        pattern_type_supporting_alt1 = re.compile('影立协字')
        pattern_type_supporting_alt2 = re.compile('影协立字')
        pattern_type_coproduction = re.compile('影合立字')
        pattern_type_coproduction_alt1 = re.compile('影立合字')
        pattern_type_coproduction_alt2 = re.compile('影合证字')
        if pattern_type_regular.search(string_regid):
            reg_type = '故事片'
        elif pattern_type_documentary.search(string_regid):
            reg_type = '纪录片'
        elif pattern_type_special.search(string_regid):
            reg_type = '特种片'
        elif pattern_type_science.search(string_regid):
            reg_type = '科教片'
        elif pattern_type_animation.search(string_regid):
            reg_type = '动画片'
        elif pattern_type_significance.search(string_regid):
            reg_type = '重大历史题材片'
        elif pattern_type_supporting.search(string_regid):
            reg_type = '协拍片'
        elif pattern_type_supporting_alt1.search(string_regid):
            reg_type = '协拍片'
        elif pattern_type_supporting_alt2.search(string_regid):
            reg_type = '协拍片'
        elif pattern_type_coproduction.search(string_regid):
            reg_type = '合拍片'
        elif pattern_type_coproduction_alt1.search(string_regid):
            reg_type = '合拍片'
        elif pattern_type_coproduction_alt2.search(string_regid):
            reg_type = '合拍片'
        else:
            reg_type = '都是什么鬼'
        RegNumber_parsed.append(reg_type)
        # 从备案号提取 年份
        pattern_reg_year = re.compile("\[[0-9][0-9][0-9][0-9]\]")
        pattern_reg_year_alt = re.compile("（[0-9][0-9][0-9][0-9]）")
        pattern_reg_year_alt2 = re.compile("【[0-9][0-9][0-9][0-9]】")
        reg_year = pattern_reg_year.search(string_regid)
        reg_year_alt = pattern_reg_year_alt.search(string_regid)
        reg_year_alt2 = pattern_reg_year_alt2.search(string_regid)
        if reg_year:
            reg_year = reg_year.group().lstrip('[').rstrip(']')
        elif reg_year_alt:
            reg_year = reg_year_alt.group().lstrip('（').rstrip('）')
        elif reg_year_alt2:
            reg_year = reg_year_alt2.group().lstrip('【').rstrip('】')
        else:
            reg_year = '查看备案号： ' + string_regid
#            print(reg_year)
        RegNumber_parsed.append(reg_year)

        # 从备案号提取 备案顺序号
        pattern_reg_orderedid = re.compile(u'第.*?号')
        pattern_reg_orderedid_alt1 = re.compile(u'][0-9].*')
        pattern_reg_orderedid_alt2 = re.compile(u'）[0-9].*号')
        reg_orderedid = pattern_reg_orderedid.search(string_regid)
        reg_orderedid_alt1 = pattern_reg_orderedid_alt1.search(string_regid)
        reg_orderedid_alt2 = pattern_reg_orderedid_alt2.search(string_regid)
        if reg_orderedid:
            reg_orderedid = reg_orderedid.group().lstrip('第').rstrip('号')
        elif reg_orderedid_alt1:
            reg_orderedid = reg_orderedid_alt1.group().lstrip(']')
        elif reg_orderedid_alt2:
            reg_orderedid = reg_orderedid_alt2.group().lstrip('）').rstrip('号')
        else:
            reg_orderedid = '查看备案号： ' + string_regid
#            print(reg_orderedid)
        RegNumber_parsed.append(reg_orderedid)
        return RegNumber_parsed
        