# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 00:34:44 2019

@author: VSurfacePro3
"""
import re

from IO_Storage import File
import MovieCN_RegtoRelease
import MovieCN_Interpreter
import pandas as pd
#%%
dir_path = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results\\"
data_reg = pd.read_csv(dir_path + 'PubTheatricalRegistration_info_allregistrations.csv')
data_rel = pd.read_csv(dir_path + 'PubThreatricalRelease_info_allreleases.csv')
#%%


# %%
getter = MovieCN_RegtoRelease.Get()
matcher = MovieCN_RegtoRelease.Match()
filt = MovieCN_RegtoRelease.Filtering()
reviewer = MovieCN_RegtoRelease.Reviewer()
record = MovieCN_RegtoRelease.Record()
compare = MovieCN_RegtoRelease.Compare()

parser = MovieCN_Interpreter.Parse()
file = File()
#%%
list_allreleases = getter.headlessRelease()
list_allregs = getter.headlessReg()
#%%
released_w_regs_imported = record.import_records() #2899
#%%
released_w_regs_now = released_w_regs_imported[:] # 2899
unmatched_releases_now = filt.unmatched_releases(released_w_regs_imported, list_allreleases) #266
unmatched_releases_now1 = filt.unmatched_releases_asymmetric(list_allreleases, released_w_regs_imported) # 261
unmatched_releases_now2 = filt.unmatched_releases_asymmetric(released_w_regs_imported, list_allreleases) # 5
unmatched_reg_now = filt.unmatched_regs(released_w_regs_imported, list_allregs) #20860
#%%
latest_pub_releases = list(filter(lambda x:x[7] == "2019-05-10", list_allreleases))
unmatched_new_releases = filt.unmatched_releases_asymmetric(latest_pub_releases, released_w_regs_now)
m_by_name = matcher.byName(unmatched_new_releases, unmatched_reg_now) # ***
m_by_pco = matcher.byPartialCompany(unmatched_new_releases, unmatched_reg_now)
m_by_pco_order = matcher.byDateOrder_inner(m_by_pco)

#%%
release_to_reg_manpower = []
release_name = list(filter(lambda x: re.match('.*我不是药神*', x[2]), released_w_regs_now))
release_name = list(filter(lambda x: re.match('.*药神.*', x[2]), unmatched_releases_now))
release_co = list(filter(lambda x: re.match('.*深圳市环球数码.*', x[3]), unmatched_releases_now)) # 公司
reg_ = list(filter(lambda x: re.match('.* 时间差.*', x[1]), list_allregs)) # 片名
reg_ = list(filter(lambda x: re.match('.*陈鸿仪.*', x[3]), list_allregs)) # 编剧
reg_ = list(filter(lambda x: re.match('.*深圳市环球数码.*', x[2]), list_allregs)) # 公司
reg_ = list(filter(lambda x: re.match('.*方春天.*', x[6]), list_allregs)) # 内容
reg_ = list(filter(lambda x: re.match('.*2010.*', x[0]), list_allregs)) # 年份
reg_ = ['影合立字[2015]第号', '美人鱼','中国电影股份有限公司', '周星驰','同意拍摄', '直备','美人鱼-2010年立项无公示档案','2010-01-01 12:00', '2010年立项无公示档案人工录入','NA']
match_releasereg = [release_name[0] + [reg_]]
release_to_reg_manpower += match_releasereg
#%%
released_w_regs_now += m_by_name
released_w_regs_now += release_to_reg_manpower
record.export(released_w_regs_now) # 2899
#%%
list_multi_reg = list(filter(lambda x:len(x[8]) > 1, released_w_regs_imported))
list_multi_reg_copro = list_multi_reg[:]

#%% Export unmatched

