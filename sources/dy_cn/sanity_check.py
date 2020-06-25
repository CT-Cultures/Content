# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from dy_Registration import Registration
import pandas as pd
import re


import numpy as np
import os
from datetime import date
from pandas.tseries.offsets import MonthEnd

dy_reg = Registration()

#%%
links_of_pages = dy_reg.links_of_pages
#%% links opublications
links_of_publications = dy_reg.links_of_publications(savefile=True) # All Records
#links_of_new_publications = dy_reg.links_of_new_publications()
#links_of_new_publications = dy_reg.links_of_new_publications(update_records=True)
#%% links of registrations
links_of_registrations = dy_reg.links_of_registrations(links_of_publications, savefile=True)
#links_of_new_registrations = dy_reg.links_of_new_registrations()
#links_of_new_registrations = dy_reg.links_of_new_registrations(update_records=True)
#%% contents of registrations
#contents_of_registrations = dy_reg.contents_of_registrations(links_of_registrations) 
#contents_of_new_registrations = dy_reg.contents_of_new_registrations() 
contents_of_new_registrations = dy_reg.contents_of_new_registrations()

#%% update_records

up_to_date_records_raw = dy_reg.update_records(save_update=False)

#%%
contents_of_registrations_raw = pd.read_csv('records/contents_of_registrations.csv', encoding='utf-8-sig')

#%%\
contents_of_registrations_raw['公示日期'].agg(dy_reg.parser.PubDate)
contents_of_registrations_raw['公示日期']

#%% Pubtitle
pubtitle = contents_of_registrations_raw['公示批次名称'].drop_duplicates().agg(dy_reg.parser.PubTitle).rename('本批次周期')
check = contents_of_registrations_raw['公示批次名称'].drop_duplicates()
#%% DateRange

def DateRange(pubttile: Series)-> datetime:
    pubtitle_unique = pubtitle.drop_duplicates().rename('本批次周期')
    pubtitle = pubtitle.to_frame()
    pubtitle['上一批次周期'] = pubtitle['本批次周期'].shift(-1)
    pubtitle['下一批次周期'] = pubtitle['本批次周期'].shift(1)
    pubtitle.fillna(value='['', '', '', '']', inplace=True)
    
    dt_range = pubtitle.agg(gen_dr, axis=1)

    def gen_dr(df_row: pd.DataFrame) -> pd.date_range:
        df_row = df_row.astype('O')
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
    
    return dt_range

test = pubtitle.agg(gen_dr, axis=1)

DateRange()

tt = (date(2010, 5, 1) + MonthEnd(1)).day
#%%
contents_of_registrations_raw['备案立项号'].agg(dy_reg.parser.RegType)

contents_of_registrations_raw[contents_of_registrations_raw['备案立项号'].isna()]
#%%
contents_of_registrations_refined = dy_reg.Refined_Records(update_first=False)
#%%
contents_of_registrations_raw['备案立项号'].agg(dy_reg.parser.RegSequenceNo)
#%%
contents_of_registrations_raw.columns





