# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 01:38:16 2019

@author: VSurfacePro3
"""
# from Standard Lib
import re
from pathlib import Path
import os
import jieba
import jieba.analyse
# from Local
import MovieCN_Interpreter
#import MovieCN_Update  # # Just to Update Records, if needed
from IO_Storage import File
#%%
class Get():
    
    def __init__(self):
        if not self:
            raise ValueError

    def headlessReg(self):
        MI = MovieCN_Interpreter.Get()
        list_regs = MI.RegInfo()
        heading_regs = ['备案立项号','片名','备案单位','编剧','备案结果',
                            '备案地','梗概','公示日期','公示批次名','公示批次链接']
        if heading_regs == list_regs[0]:
            list_regs = list_regs[1:]
        return list_regs

    def headlessRelease(self):
        MI = MovieCN_Interpreter.Get()
        # Get Release Records
        list_releases = MI.ReleaseInfo()
        headings_releases = ['编码','公映证号','片名','第一出品单位','批次名称',
                                  '公示批次中的序号','批次链接','发布日期']
        if headings_releases == list_releases[0]:
            list_releases = list_releases[1:]
        return list_releases
    
class Filtering():
    
    def __init__(self):
        if not self:
            raise ValueError

    def unmatched_releases(self, records_matched, records_before_match):
        rmatched = tuple(map(lambda x:x[0:8], records_matched))
        rmatched = tuple(map(lambda x:tuple(x), rmatched))
        rbfmatch = tuple(map(lambda x:x[0:8], records_before_match))
        rbfmatch = tuple(map(lambda x:tuple(x), rbfmatch))
        records_unmatched = tuple(set(rmatched).symmetric_difference(set(rbfmatch)))
        records_unmatched = list(map(lambda x:list(x), records_unmatched))
        return records_unmatched
    
    def unmatched_releases_asymmetric(self, records_set, records_pool):
#        records_set = latest_pub_releases[:]
#        records_pool = released_w_regs_now[:]
        r_set = tuple(map(lambda x:x[0:8], records_set))
        r_set = list(map(lambda x:tuple(x), r_set))
        r_pool = tuple(map(lambda x:x[0:8], records_pool))
        r_pool = list(map(lambda x:tuple(x), r_pool))
        index = 0
        while index < len(r_set):
            for pool_record in r_pool:
                if r_set[index] == pool_record:
                    del r_set[index]
                    index = index - 1
                    break
            index = index + 1
        r_set = list(map(lambda x:list(x), r_set))
        return r_set

    def unmatched_listoflist_asymmetric(self, records_set, records_pool):
#        records_set = rsig_wbo[:]
#        records_pool = rsig[:]
        r_set = list(map(lambda x:x[0:4], records_set))
        r_set = list(map(lambda x:tuple(x), r_set))
        r_pool = list(map(lambda x:tuple(x), records_pool))
        index = 0
        while index < len(r_pool):
            for set_record in r_set:
                if r_pool[index] == set_record:
                    del r_pool[index]
                    index = index - 1
                    break
            index = index + 1
        r_pool = list(map(lambda x:list(x), r_pool))
        return r_pool

    def unmatched_regs(self, records_matched, records_regs):
        regs_w_matches = map(lambda x:x[8], records_matched)
        unwrapped = []
        for each in regs_w_matches:
            unwrapped += each
        unwrapped = tuple(map(lambda x:tuple(x),  unwrapped))
        records_regs = tuple(map(lambda x:tuple(x),  records_regs))
        compared = tuple(set(records_regs).symmetric_difference(set(unwrapped)))
        compared = list(map(lambda x:list(x), compared))
        return compared
    
    def checknum_regtaken(self, records_matched):
        length = 0
        for record in records_matched:
            length += len(record[8])
        return length
    
    def check_regtaken(self, records_matched):
        reg_taken = []
        for record in records_matched:
            for reg in record[8]:
                reg_taken += [reg]
        return reg_taken
    
    def check_duplicates(self, list_to_check):
        list_in_tuple = tuple(map(lambda x:tuple(x),  list_to_check))
        seen = {}
        dupes = []
        for x in list_in_tuple:
            if x not in seen:
                seen[x] = 1
            else:
                if seen[x] == 1:
                    dupes.append(x)
                seen[x] += 1
        return dupes
    
    def remove_duplicated_unfold_matchedreg(self, records_matched):
        unfolded = []
        for release in records_matched:
            rmdup = (map(lambda x:tuple(x), release[8]))
            rmdup = set(rmdup)
            release[8] = list(map(lambda x:list(x), rmdup))
            for reg in release[8]:
                unfolded += [release[0:8] + [reg]]
        print("Records: ", str(len(records_matched)), ", ", "unfolded to: ", str(len(unfolded)), " without reg duplicates.")
        return unfolded
    
    def wrap_multireg_matchedreg(self, records_matched_unfolded, removeduplicates=False):
        wrapped = []
        i = 0
        while i < len(records_matched_unfolded)-1:
            reg_combined = []
            j= i+1
            while j < len(records_matched_unfolded):
                if records_matched_unfolded[j][1:8] == records_matched_unfolded[i][1:8]:
                    reg_combined += [records_matched_unfolded[j][8]]
                    del records_matched_unfolded[j]
                    j = j - 1
                j = j + 1
            reg_combined = [records_matched_unfolded[i][8]] + reg_combined
            wrapped += [records_matched_unfolded[i][0:8] + [reg_combined]]
            i = i + 1
        if removeduplicates:
            for each in wrapped[8]:
                remdup = tuple(map(lambda x:tuple(x), wrapped[8]))
                remdup = set(remdup)
                wrapped[8] = list(map(lambda x:list(x), remdup))        
        return wrapped
        
    
class Compare():
    
    def regs(self, reg1, reg2):
        reg1_tuple = tuple(map(lambda x:tuple(x), reg1))
        reg2_tuple = tuple(map(lambda x:tuple(x), reg2))
        compared = tuple(set(reg1_tuple).symmetric_difference(set(reg2_tuple)))
        compared = list(map(lambda x:list(x), compared))
        return compared
       
    def releases_w_reg(self, rwr1, rwr2):
        rwr1_tuple = tuple(map(lambda x:tuple(x), rwr1))
        rwr2_tuple = tuple(map(lambda x:tuple(x), rwr2))    
        compared = tuple(set(rwr1_tuple).symmetric_difference(set(rwr2_tuple)))
        compared = list(map(lambda x:list(x), compared))
        return compared        
    
class Match():  
       
    def byName(self, records_released, list_regs_wo_heading):
        released_with_reg = []
        if len(list_regs_wo_heading) != 0 and len(records_released) !=0:
            for release in records_released:
                release_reg_match = list(filter(lambda x:x[1] == release[2], list_regs_wo_heading))
                if release_reg_match:
                    released_with_reg += [release[0:8] + [release_reg_match]]
            return released_with_reg       
        
    def Unmatched_byName(self, records_released, list_regs_wo_heading):    
        if len(list_regs_wo_heading) != 0 and len(records_released) !=0:
            released_with_unknownreg = []
            for release in records_released:
                release_reg_match = list(filter(lambda x:x[1] == release[2], list_regs_wo_heading))
                if not release_reg_match:
                    released_with_unknownreg += [release]
            return released_with_unknownreg     
        
    def byPartialName(self, records_released, list_regs_wo_heading):
        PN_matches = []
        if len(records_released) != 0:
            for release in records_released:
                str_to_match = r".*" + release[2] + r".*"
#                print(str_to_match)
                match_partialname = list(filter(lambda x: re.match(str_to_match, x[1]), list_regs_wo_heading)) # 用片名                    
                if len(match_partialname) !=0:
                    PN_matches += [release[0:8] + [match_partialname]]
        return PN_matches

    def byPartialName_inner(self, records_released):
        PN_matches = []
        if len(records_released) != 0:
            for release in records_released:
                rel = [release[0:8]]
                reg = release[8]
                match = self.byPartialName(rel, reg)
                if len(match) != 0:
                    PN_matches += match
            return PN_matches
  
    def bySegName(self, records_released, list_regs_wo_heading):
        seg_matched = []
        if len(records_released) != 0:
            for release in records_released:
                name_seg = list(jieba.cut(release[2], cut_all=False))
                rel_seg_match = []
                for seg in name_seg:
                    str_to_match = r".*" + seg + r".*"
                    match =list(filter(lambda x: re.match(str_to_match, x[1]), list_regs_wo_heading))
                    if len(match) != 0:
                        rel_seg_match +=match
                seg_matched += [release[0:8] + [rel_seg_match]]
        return seg_matched
    
   
    def byKeywordsName(self, records_released, list_regs_wo_heading):
        kw_matched = []
        if len(records_released) != 0:
            for release in records_released:
                keywords = jieba.analyse.extract_tags(release[2])
                rel_kw_match = []
                for keyword in keywords:
                    str_to_match = r".*" + keyword + r".*"
                    match =list(filter(lambda x: re.match(str_to_match, x[1]), list_regs_wo_heading))
                    if len(match) != 0:
                        rel_kw_match +=match
                if len(rel_kw_match) != 0:
                    kw_matched += [release[0:8] + [rel_kw_match]]               
        return kw_matched  

    def byKeywordsName_inner(self, records_released):
        kw_matched = []
        for release in records_released:
            rel = [release[0:8]]
            reg = release[8]
            match = self.byKeywordsName(rel, reg)
            if len(match) != 0:
                kw_matched += match
        return kw_matched      
    
    def byPartialCompany(self, records_released, list_regs_wo_heading):
        PC_matches = []
        if len(records_released) != 0 and len(list_regs_wo_heading) != 0:
            for release in records_released:
                release_3 = re.sub("\(", r"\(", release[3])
                release_3 = re.sub("\)", r"\)", release_3)
                str_to_match = '.*' + release_3 + '.*'
#                print(str_to_match)
                match_partialcompany = list(filter(lambda x: re.match(str_to_match, x[2]), list_regs_wo_heading)) # 用备案方                  
                if len(match_partialcompany) !=0:
                    PC_matches += [release[0:8] + [match_partialcompany]]
        return PC_matches
    
    def byPartialCompany_inner(self, records_released):
        PC_matches = []
        for release in records_released:
            rel = [release[0:8]]
            reg = release[8]
            match = self.byPartialCompany(rel, reg)
            if len(match) != 0:
                PC_matches += match
        return PC_matches    
    
    def byKeywordsCompany(self, records_released, list_regs_wo_heading):
        stopwords = ['公司', '有限公司', '股份有限公司', '投资有限公司', 
                     '传播', '传媒', 
                     '文化', '文化传媒', '文化传播', '文化发展',
                     '影视', '影视文化', '影视发展','影视传媒', '影视制作', '影视公司',
                     '影业', '影业有限公司',
                     '发展', '发展有限公司']
        kw_matched = []
        if len(records_released) != 0:
            for release in records_released:
                keywords = jieba.analyse.extract_tags(release[3])
                rel_kw_match = []
                for keyword in keywords:
                    stopword_match = 0
                    for word in stopwords:
                        if keyword == word:
                            stopword_match += 1
                    if stopword_match == 0:
                        str_to_match = r".*" + keyword + r".*"
                        match =list(filter(lambda x: re.match(str_to_match, x[2]), list_regs_wo_heading))
                        if len(match) != 0:
                            rel_kw_match +=match
                if len(rel_kw_match) != 0:
                    kw_matched += [release[0:8] + [rel_kw_match]]               
        return kw_matched
    
    def byKeywordsCompany_inner(self, records_released):
        PC_matches = []
        for release in records_released:
            rel = [release[0:8]]
            reg = release[8]
            match = self.byPartialCompany(rel, reg)
            if len(match) != 0:
                PC_matches += match
        return PC_matches 
    
    def byRegthenReleaseOrder(self, records_released, list_regs_wo_heading):
        RtRO_matches = []
        parser = MovieCN_Interpreter.Parse()
        if len(records_released) != 0 and len(list_regs_wo_heading) != 0:
            for release in records_released:
                dt_release = parser.IssueDate(release[7].rstrip())
                match_byreqorder = list(filter(lambda x: parser.PubDate(x[7].rstrip()) < dt_release, list_regs_wo_heading))
                if len(match_byreqorder) !=0:
                    RtRO_matches += [release[0:8] + [match_byreqorder]]
        return RtRO_matches
    
    def byDateOrder_inner(self, records_released):
        DO_matches = []
        for release in records_released:
            rel = [release[0:8]]
            reg = release[8]
            match = self.byRegthenReleaseOrder(rel, reg)
            if len(match) != 0:
                DO_matches += match
        return DO_matches
    
    def by_KeywordsName_to_RegDescription(self, records_released, list_regs_wo_heading):
        kw_matched = []
        if len(records_released) != 0:
            for release in records_released:
                keywords = jieba.analyse.extract_tags(release[2])
                rel_kw_match = []
                for keyword in keywords:
                    str_to_match = r".*" + keyword + r".*"
                    match =list(filter(lambda x: re.match(str_to_match, x[6]), list_regs_wo_heading))
                    if len(match) != 0:
                        rel_kw_match +=match
                if len(rel_kw_match) != 0:
                    kw_matched += [release[0:8] + [rel_kw_match]]               
        return kw_matched
    
    def by_KeywordsName_to_RegDescription_inner(self, records_released):
        kw_matched = []
        for release in records_released:
            rel = [release[0:8]]
            reg = release[8]
            match = self.by_KeywordsName_to_RegDescription(rel, reg)
            if len(match) != 0:
                kw_matched += match
        return kw_matched       
    
class Reviewer():
    
    def __init__(self):
        if not self:
            raise ValueError

    def byHuman_inprompt(self, records_released_w_match):
        records_reviewed = []
        for release in records_released_w_match:
            print("\nRelease is: ", release[0:8], "\n", "Potential Matches: ")
            index = 0
            while index < len(release[8]):           
                print("[", index, "]: ", "\n", release[8][index])
                index = index + 1
            index_selection = input("Enter Selection: ").split(',')
            if len(index_selection) == 0:
                break
            regupdated = []
            for selection in index_selection:
                if selection != 'none':
                    regupdated += [release[8][int(selection)]]
                    records_reviewed += [release[0:8] + [regupdated]]
        return records_reviewed
    
    def export(self, released_w_reg_toreview, removeduplicates=False):
        unfolded = []
        for release in released_w_reg_toreview:
            if removeduplicates:
                rmdup = (map(lambda x:tuple(x), release[8]))
                rmdup = set(rmdup)
                release[8] = list(map(lambda x:list(x), rmdup))
            for reg in release[8]:
                unfolded += [release[0:8] + [reg]]
        file = File()
        filename = "released_w_reg_toreview"
        dir_root_wip = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\wip"
        file.write_to_cvs(unfolded, dir_root_wip, filename)
        showtext = ("Review file exported, number of records: " + str(len(released_w_reg_toreview)) 
                    + ", unfolded to: " + str(len(unfolded)) + ".")
        return showtext
        
    def import_reviewed(self, removeduplicates= False):
        file = File()
        filepath = Path(r'C:\Users\VSurfacePro3\Desktop\Degree Classes\Trade University\CTAI\R_looklook\wip\released_w_reg_toreview.csv')
        importedfile = file.open_to_list_of_list(filepath)
        importedfile = list(map(lambda x:x[0:8]+[eval(x[8])], importedfile))
        wrapped = []
        i = 0
        while i < len(importedfile)-1:
            reg_combined = []
            j= i+1
            while j < len(importedfile):
                if importedfile[j][1:8] == importedfile[i][1:8]:
                    reg_combined += [importedfile[j][8]]
                    del importedfile[j]
                    j = j - 1
                j = j + 1
            reg_combined = [importedfile[i][8]] + reg_combined
            wrapped += [importedfile[i][0:8] + [reg_combined]]
            i = i + 1
        if removeduplicates:
            for each in wrapped[8]:
                remdup = tuple(map(lambda x:tuple(x), wrapped[8]))
                remdup = set(remdup)
                wrapped[8] = list(map(lambda x:list(x), remdup))        
        return wrapped
# =============================================================================
#                 
#         while index < len(importedfile)-1:
#             if importedfile[index][0:8] == importedfile[index+1][0:8]:
#                 wrapped += [importedfile[index][0:8] + [[importedfile[index][8]] + [importedfile[index+1][8]]]]
#             index = index + 1
# =============================================================================
        os.remove(filepath) # delete reviewed file after import
        return wrapped              

class Record(object):
    
    def __init__(self):
        if not self:
            raise ValueError

    def export(self, released_w_reg):
        file = File()
        filename = "Release_w_Reg"
        dir_root_results = "C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results"
        file.write_to_cvs_wbk(released_w_reg, dir_root_results, filename)
        showtext = "Release_w_reg.csv exported, total number of records: " + str(len(released_w_reg)) + "."
        return showtext
    
    def import_records(self):
        file = File()
        filepath = Path(r'C:\Users\VSurfacePro3\Desktop\Degree Classes\Trade University\CTAI\R_looklook\results\Release_w_Reg.csv')
        importedfile = file.open_to_list_of_list(filepath)
        importedfile = list(map(lambda x:x[0:8]+[eval(x[8])], importedfile))
        return importedfile

    def w_namechange_formatted(self, released_w_reg, heading=False):
        getter = MovieCN_Interpreter.Get()
        reg_PubIssue_daterange = getter.List_PubIssue_DateRange()
        records_to_study = []   
        for release in released_w_reg:
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
        return records_to_study
##############################################################################
