# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 02:17:05 2019

@author: VSurfacePro3
"""
# from standard Lib
import re
import jieba
from pathlib import Path

# from local Lib
from IO_Storage import File
import MovieCN_RegtoRelease
import MovieCN_Interpreter
import CrawlCleaner
#%%
getter = MovieCN_RegtoRelease.Get()
matcher = MovieCN_RegtoRelease.Match()
filt = MovieCN_RegtoRelease.Filtering()
reviewer = MovieCN_RegtoRelease.Reviewer()
record = MovieCN_RegtoRelease.Record()
compare = MovieCN_RegtoRelease.Compare()
cleaner = CrawlCleaner.ChineseCleaner()
parser = MovieCN_Interpreter.Parse()
file = File()
exporter = File()
getterMint = MovieCN_Interpreter.Get()
# %%
# 加载票房数据
dir_result_root = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
path_project = 'tostudy\\Effects of Name Change'
filename = '01 records_forwardmatch'
rf = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = '02 records_backwardmatch'
rb = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = '03 records_kwnamematch'
rkw = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = '04 records_significantnamechange'
rsig = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'CBOOO_BO_CN'
bo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
bo = bo[1:]
#%%
# 加载 tostudy 数据
dir_result_root = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
path_project = '\\tostudy\\Effects of Name Change'
filename = 'r_wonamechange_wbo'
r_wonamechange_wbo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'rf_wbo'
rf_wbo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'rb_wbo'
rb_wbo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'rkw_wbo'
rkw_wbo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'rsig_wbo'
rsig_wbo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
filename = 'CBOOO_BO_CN'
bo = file.open_to_list_of_list(Path(dir_result_root + "\\" + path_project + "\\" + filename + ".csv"))
bo = bo[1:]
#%% 获取有改名影片的票房
bosig = list(filter(lambda x:x[4] != '', bo))
bosig = list(filter(lambda x:x[4] != '0', bosig))
rsig_wbo = []
for bor in bosig:
    for rc in rsig:
        if cleaner.Remove_Punctuation(rc[0]) == cleaner.Remove_Punctuation(bor[1]):
            rsig_wbo += [rc + [bor[4]]]
rsig_wobo = filt.unmatched_listoflist_asymmetric(rsig_wbo, rsig)

rf_wbo = []
for bor in bosig:
    for rc in rf:
        if cleaner.Remove_Punctuation(rc[0]) == cleaner.Remove_Punctuation(bor[1]):
            rf_wbo += [rc + [bor[4]]]
rf_wobo = filt.unmatched_listoflist_asymmetric(rf_wbo, rf)

rb_wbo = []
for bor in bosig:
    for rc in rb:
        if cleaner.Remove_Punctuation(rc[0]) == cleaner.Remove_Punctuation(bor[1]):
            rb_wbo += [rc + [bor[4]]]
rb_wobo = filt.unmatched_listoflist_asymmetric(rb_wbo, rb)

rkw_wbo = []
for bor in bosig:
    for rc in rkw:
        if cleaner.Remove_Punctuation(rc[0]) == cleaner.Remove_Punctuation(bor[1]):
            rkw_wbo += [rc + [bor[4]]]
rkw_wobo = filt.unmatched_listoflist_asymmetric(rkw_wbo, rkw)

#%%
# 人工调整
#list(filter(lambda x: re.match('.*新港故事.*', x[1]), bosig)) 
#to_insert = r_wonamechange_wobo[297]; del r_wonamechange_wobo[297]
#to_insert.append('105178')
#r_wonamechange_wbo.append(to_insert) #巨齿鲨
release_name_bo = list(filter(lambda x: re.match('.*杀破狼·贪狼.*', x[1]), bo)) # 片名 52157

# %%
list_allreleases = getter.headlessRelease()
list_allregs = getter.headlessReg()
released_w_regs_imported = record.import_records() #2854
released_w_regs_now = released_w_regs_imported[:] # 2854
#unmatched_releases_now = filt.unmatched_releases(released_w_regs_imported, list_allreleases) #257
#unmatched_releases_now1 = filt.unmatched_releases_asymmetric(list_allreleases, released_w_regs_imported) # 252
#unmatched_releases_now2 = filt.unmatched_releases_asymmetric(released_w_regs_imported, list_allreleases) # 5
#unmatched_reg_now = filt.unmatched_regs(released_w_regs_imported, list_allregs) #20712
#%%
# 获取未改名影片的票房
joined_w_bo = rf_wbo + rb_wbo + rkw_wbo + rsig_wbo
joined_w_namechange = rf + rb + rkw + rsig

released_w_regs_wonamechange = released_w_regs_imported[:]
index = 0
while index < len(released_w_regs_wonamechange):
    for set_record in joined_w_namechange:
        if cleaner.Remove_Punctuation(set_record[0]) == cleaner.Remove_Punctuation(released_w_regs_wonamechange[index][2]):
            del released_w_regs_wonamechange[index]
            index = index - 1
            break
    index = index + 1
r_wonamechange = record.w_namechange_formatted(released_w_regs_wonamechange)
r_wonamechange_wbo = []
for bor in bosig:
    for rc in r_wonamechange:
        if cleaner.Remove_Punctuation(rc[0]) == cleaner.Remove_Punctuation(bor[1]):
            r_wonamechange_wbo += [rc + [bor[4]]]
r_wonamechange_wobo = filt.unmatched_listoflist_asymmetric(r_wonamechange_wbo, r_wonamechange)
#%%
# 输出 带 bo 档案
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results\\tostudy'
filename = 'rf_wbo'
exporter.write_to_cvs(rf_wbo, dir_path, filename)
filename = 'rb_wbo'
exporter.write_to_cvs(rb_wbo, dir_path, filename)
filename = 'rkw_wbo'
exporter.write_to_cvs(rkw_wbo, dir_path, filename)
filename = 'rsig_wbo'
exporter.write_to_cvs(rsig_wbo, dir_path, filename)
filename = 'r_wonamechange_wbo'
exporter.write_to_cvs(r_wonamechange_wbo, dir_path, filename)

#%%
# 只看 改过名字的影片， 片名 release【2】， reg【1]
released_w_namechange = []
for release in released_w_regs_now:
    rel_name = release[2]
    reg_records = release[8]
    num_change = 0
    for reg in reg_records:
        if reg[1] != rel_name:
            num_change += 1
    if num_change > 0:
        released_w_namechange += [release]
del rel_name
del reg_records
del num_change
del reg
#%%
# 过滤掉非故事片或合拍片
released_w_name_change_drama = []
for release in released_w_namechange:
    reg_records = release[8]
    for reg in reg_records:
        reg_id_parsed = parser.RegID(reg[0])
        if (reg_id_parsed[0] == '故事片' 
            or reg_id_parsed[0] == '合拍片'
            or reg_id_parsed[0] == '动画片'
            or reg_id_parsed[0] == '特种片'):
            released_w_name_change_drama += [release]
del reg_records
del reg_id_parsed  
del reg     
del release     
#%%        
# 生成初步 研究对象数据库
reg_PubIssue_daterange = getter.List_PubIssue_DateRange()
records_to_study = []   
for release in released_w_name_change_drama:
    rel_name = release[2]
    rel_pubdate = release[7]
    reg_records = release[8]
    reg_parts = []
    for reg in reg_records:
        reg_name = reg[1]
        #reg_pubdate = reg[7]
        reg_pubtitle = reg[8]
        for pubissue in reg_PubIssue_daterange:
            if pubissue[0] == reg_pubtitle:
                reg_issuedate = pubissue[1]
        #reg_pubtitle = parser.PubTitle(reg_pubtitle)
        reg_parts += reg_name, reg_issuedate
    records_to_study += [[rel_name, rel_pubdate, reg_parts[0], reg_parts[1]]]
#heading = ['公映许可通过名称', '公映许可公示日期', '备案名称', '备案覆盖起始期']
heading = False
if heading:
    records_to_study = [heading] + records_to_study
del release
del rel_name
del rel_pubdate
del reg_PubIssue_daterange
del reg
del reg_name
del reg_records
del reg_parts
del reg_pubtitle
del pubissue
del reg_issuedate
#%%
# 新名从含旧 缩短的
records_w_partialnamematch_forward = list(filter(lambda x:re.match(str(".*" + x[0] + ".*"), x[2]), records_to_study)) # 片名部分相同
comp1 = tuple(map(lambda x:tuple(x), records_to_study))
comp2 = tuple(map(lambda x:tuple(x), records_w_partialnamematch_forward))
records_remain = list(set(comp1).symmetric_difference(set(comp2)))
#%%
# 新名在救命基础上 扩展的
records_w_partialnamematch_backward = list(filter(lambda x:re.match(str(".*" + x[2] + ".*"), x[0]), records_remain))
comp1 = tuple(map(lambda x:tuple(x), records_w_partialnamematch_backward))
comp2 = tuple(map(lambda x:tuple(x), records_remain))
records_remain1 = list(set(comp1).symmetric_difference(set(comp2)))
# %%
# 新旧名元素相关的
records_w_pname_kw = []
for record in records_remain1:
    kw_rel = jieba.analyse.extract_tags(record[0])
    kw_reg = jieba.analyse.extract_tags(record[2])
    for kwrel in kw_rel:
        for kwreg in kw_reg:
            if kwrel == kwreg:
                records_w_pname_kw += [record]
records_w_pname_kw = list(set(tuple(records_w_pname_kw)))
comp1 = tuple(map(lambda x:tuple(x), records_w_pname_kw))
comp2 = tuple(map(lambda x:tuple(x), records_remain1))
records_remain3 = list(set(comp1).symmetric_difference(set(comp2)))
# %%
# %%
dir_path = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
filename = 'CBOOO_BO_CN'
filepath = Path(dir_path + "\\" + filename + '.csv')
cbooo_records = file.open_to_list_of_list(filepath) #name at [1]
#%% 输出

        
