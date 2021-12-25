# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 03:07:32 2020

@author: VSurfacePro3
"""

#%% Import Packages
from Record_Registration import Registration
import pandas as pd
import re
import matplotlib as mp
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 9]
mp.rcParams['font.sans-serif'] = ['KaiTi']
import math
from datetime import timedelta

import numpy as np
import os

dy_reg = Registration()
#%%
links_of_pages = dy_reg.links_of_pages()

#%%
links_of_pages = dy_reg.links_of_pages()
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

#%% Raw Records
contents_of_registrations_raw = pd.read_csv('records/contents_of_registrations.csv', encoding='utf-8-sig')

#%% Refined Records
contents_of_registrations_refined = dy_reg.Refined_Records(update_first=False)

#%% Columns
contents_of_registrations_refined.columns
dtype = {   '备案立项号': 'str',
            '片名': 'str', 
            '备案单位': 'str',
            '编剧': 'str',
            '备案结果': 'str',
            '备案地': 'str',
            '梗概': 'str',
            '公示日期': 'datetime64[ns]',
            '公示批次名称': 'str',
            '制作表链接': 'str',
            '公示批次链接': 'str',
            '公示年': 'Int64',
            '公示批次起始': 'str',
            '类型': 'str',
            '备案申请年份': 'int64',
            '备案立项年度顺序号': 'Int64',
            '公示覆盖期间': 'object',
            '公示覆盖天数': 'int64'
         }
#%%

def complete_dt_by_year_by_type(df):
    df_copy = df.copy()
    df_copy['备案公示日期预测'] = np.nan
    df_copy['备案通过日偏差'] = np.nan
    df_tmp = df_copy.loc[:,['备案申请年份', '类型','备案立项年度顺序号','公示日期']]
    df_tmp.set_index(['备案申请年份', '类型'], inplace=True)
    #df_tmp = df_tmp.sort_values(by=['备案申请年份', '类型','备案立项年度顺序号'], ascending=True)
    df_tmp = df_tmp.sort_index(level=0)
    indicies = df_tmp.index.unique()
    for idx in indicies:
        if np.nan in idx:
            continue
        else:
            #print(idx)
            df1 = df_tmp.loc[idx,:]
            if df1.shape[0] > 1:
                #df1 = df1.sort_values(by='备案立项年度顺序号', ascending=True)
                df_dt = dy_reg.estimate.complete_dt(df1)
                df_merged = pd.merge(df, df_dt, on=['备案申请年份', '类型', '备案立项年度顺序号'], how='left')
                df_copy.update(df_merged)
    return df_copy

testing = complete_dt_by_year_by_type(contents_of_registrations_refined)




df_copy = contents_of_registrations_refined.copy()
df_copy['备案公示日期预测'] = np.nan
df_copy['备案通过日偏差'] = np.nan
df_tmp = df_copy.loc[:,['备案申请年份', '类型','备案立项年度顺序号','公示日期']]
df_tmp.set_index(['备案申请年份', '类型'], inplace=True)
df_tmp = df_tmp.sort_index(level=0)
indicies = df_tmp.index.unique()

for idx in indicies:
    if np.nan in idx:
        continue
    else:
        df1 = df_tmp.loc[idx,:]
        print(df1)

df_dt = dy_reg.estimate.complete_dt(df1)
df_merged = pd.merge(contents_of_registrations_refined, df_dt, on=['备案申请年份', '类型', '备案立项年度顺序号'], how='left')

contents_of_registrations_refined.dtypes
# quantile problem

contents_of_registrations_refined[contents_of_registrations_refined['备案申请年份'].isna()]
