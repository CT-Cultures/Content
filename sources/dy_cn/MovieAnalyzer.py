# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 17:29:57 2019
@author: VX
"""
import re
import datetime
from datetime import
import calendar
from pathlib import Path
from operator import itemgetter
#import Numpy as np
from IO_Storage import File
import MovieCN
import Mtime
#%%

class Clean(object):  # used to handle exceptions from web sources
    def __init__(self):
        if not self:
            raise ValueError

    def correct_Regerror(self, info_reg):
        pubtitle_error_corrector = {
         '国家新闻出版广电总局电影局关于2011年10月全国电影剧本（梗概）备案、立项公示的通知':
         '国家新闻出版广电总局电影局关于2015年04月（上旬）全国电影剧本（梗概）备案、立项公示的通知',
         '广电总局电影局关于2017年11月（下旬）全国电影剧本（梗概）备案、立项公示的通知':
         '广电总局电影局关于2011年11月（下旬）全国电影剧本（梗概）备案、立项公示的通知',
         '广电总局电影局关于2011年06月（下旬）全国电影剧本（梗概）备案、立项公示的通知':
         '广电总局电影局关于2012年06月（下旬）全国电影剧本（梗概）备案、立项公示的通知'}
        pos_reg = 0
        info_reg1 = list(info_reg)
        while pos_reg < len(info_reg1):
            for error, corrector in pubtitle_error_corrector.items():
                if error == info_reg1[pos_reg][8]:
                    info_reg1[pos_reg][8] = corrector
            pos_reg = pos_reg + 1
        return info_reg1

class Get(object):
    def __init__(self):
        if not self:
            raise ValueError

    def RegInfo(self):
        reader = File()
        cleaner = Clean()
        filepath = Path(r'C:\Users\VSurfacePro3\Desktop\Degree Classes\Trade University\CTAI\R_looklook\results\PubTheatricalRegistration_info_allregistrations.csv')
        info_reg = reader.open_to_list_of_list(filepath)
        info_reg = cleaner.correct_Regerror(info_reg)
        return info_reg

    def RegPub_SortedTitleDate(self):
        info_reg = self.RegInfo()
        extracter = Extract()
        col_title = extracter.columnfromlistoflist(info_reg, 8)
        col_title = list(set(col_title[1:len(col_title)]))
        pos_title = 0
        title_and_date = []
        parser = Parse()
        while pos_title < len(col_title):
            pos_reg = 0
            while pos_reg < len(info_reg):
                if col_title[pos_title] == info_reg[pos_reg][8]:
                    title_and_date.append([col_title[pos_title], str(parser.PubDate(info_reg[pos_reg][7]))])
                    break
                pos_reg = pos_reg + 1
            pos_title = pos_title + 1
        sorted_title_by_date = sorted(title_and_date, key=itemgetter(1))
        return sorted_title_by_date

    def List_PreviousPubDate(self):
        sorted_title_by_date = self.RegPub_SortedTitleDate()
        pos_title = 0
        list_previous_pubdate = []
        row = [sorted_title_by_date[pos_title][0], sorted_title_by_date[pos_title][1], 'No Previous Publications', 'No Previous Publication Date']
        pos_title = 1
        list_previous_pubdate += [row]
        while pos_title < len(sorted_title_by_date):
            row = [sorted_title_by_date[pos_title][0], sorted_title_by_date[pos_title][1],
                   sorted_title_by_date[pos_title-1][0], sorted_title_by_date[pos_title-1][1]]
            list_previous_pubdate += [row]
            pos_title = pos_title + 1
        return list_previous_pubdate

    def List_PreviousPubIssue(self):
        sorted_title_by_date = self.RegPub_SortedTitleDate()
        pos_title = 0
        parser = Parse()
        list_previous_pubissue = []
        row = [parser.PubTitle(sorted_title_by_date[pos_title][0]), sorted_title_by_date[pos_title][1], 'No Previous Publications', 'No Previous Publication Date']
        pos_title = 1
        list_previous_pubissue += [row]
        while pos_title < len(sorted_title_by_date):
            row = [parser.PubTitle(sorted_title_by_date[pos_title][0]), sorted_title_by_date[pos_title][1],
                   parser.PubTitle(sorted_title_by_date[pos_title-1][0]), sorted_title_by_date[pos_title-1][1]]
            list_previous_pubissue += [row]
            pos_title = pos_title + 1
        return  list_previous_pubissue

    def List_PubIssue_DateRange(self):
#        list_previous_pubissue = self.List_PreviousPubIssue()
        getter = Get()
        list_previous_pubissue = getter.List_PreviousPubIssue()
        list_previous_pubdate = getter.List_PreviousPubDate()

        list_pubissue_daterange = []
        # Process First Issue
# 年 月 部分的处理
        pos_issue = 0
        year = list_previous_pubissue[pos_issue][0][0]
        month = list_previous_pubissue[pos_issue][0][1]
        month_items = month.split('、')
        if len(month_items) == 1:
            start_month = month_items[0]
            end_month = month_items[0]
        elif len(month_items) == 2:
            start_month = month_items[0]
            end_month = month_items[1]
# 对于 旬 的处理
        if list_previous_pubissue[pos_issue][0][2] == '上旬':
            start_day = 1
            if list_previous_pubissue[pos_issue+1][0][2] == '中旬' or list_previous_pubissue[pos_issue+1][0][2] == '中旬、下旬':
                end_day = 15  # or 10 如果有中旬
            else:
                end_day = 10
        elif list_previous_pubissue[pos_issue][0][2] == '上旬、中旬':
            start_day = 1
            end_day = 20
        elif list_previous_pubissue[pos_issue][0][2] == '中旬':
            start_day = 11
            end_day = 20
        elif list_previous_pubissue[pos_issue][0][2] == '中旬、下旬':
            start_day = 11
            end_day = calendar.monthrange(int(year), int(start_month))[1]
        elif list_previous_pubissue[pos_issue][0][2] == '下旬': # 不用检查，没有上一期
            start_day = 16
            end_day = calendar.monthrange(int(year), int(start_month))[1]
        elif list_previous_pubissue[pos_issue][0][2] == '下旬、上旬': # 不用检查，没有上一期
            start_day = 16
            end_day = calendar.monthrange(int(year), int(end_month))[1]
        rendered_startday = datetime.date(int(year), int(start_month), int(start_day))
        rendered_endday = datetime.date(int(year), int(end_month), int(end_day))
        row = [list_previous_pubdate[pos_issue][0], str(rendered_startday), str(rendered_endday)]
        list_pubissue_daterange += [row]

        # Process Remaining Issues， except the last one
        pos_issue = 1
        while pos_issue < (len(list_previous_pubissue)-1):
            year = list_previous_pubissue[pos_issue][0][0]
            month = list_previous_pubissue[pos_issue][0][1]
            month_items = month.split('、')
            if len(month_items) == 1:
                start_month = month_items[0]
                end_month = month_items[0]
            elif len(month_items) == 2:
                start_month = month_items[0]
                end_month = month_items[1]
            if list_previous_pubissue[pos_issue][0][2] == '没有旬':
                start_day = 1
                end_day = calendar.monthrange(int(year), int(end_month))[1]
            elif list_previous_pubissue[pos_issue][0][2] == '上旬':
                start_day = 1
                if list_previous_pubissue[pos_issue+1][0][2] == '中旬': #检查下一期
                    end_day = 10
                elif list_previous_pubissue[pos_issue+1][0][2] == '中旬、下旬':
                    end_day = 10  # or 10 如果有中旬
                else:
                    end_day = 15
            elif list_previous_pubissue[pos_issue][0][2] == '上旬、中旬':
                start_day = 1
                end_day = 20
            elif list_previous_pubissue[pos_issue][0][2] == '中旬':
                start_day = 11
                end_day = 20
            elif list_previous_pubissue[pos_issue][0][2] == '中旬、下旬':
                start_day = 11
                end_day = calendar.monthrange(int(year), int(end_month))[1]
            elif list_previous_pubissue[pos_issue][0][2] == '下旬':
                if list_previous_pubissue[pos_issue][2][2] == '上旬、中旬': #检查上一期
                    start_day = 21
                    end_day = calendar.monthrange(int(year), int(end_month))[1]
                elif list_previous_pubissue[pos_issue][2][2] == '中旬':
                    start_day = 21
                    end_day = calendar.monthrange(int(year), int(end_month))[1]
                else:
                    start_day = 16
                    end_day = calendar.monthrange(int(year), int(end_month))[1]
            elif list_previous_pubissue[pos_issue][0][2] == '下旬、上旬':
                if list_previous_pubissue[pos_issue][2][2] == '上旬': #检查上一期
                    start_day = 16
                else:
                    start_day = 21
                if list_previous_pubissue[pos_issue+1][0][2] == '中旬': #检查下一期
                    end_day = 10
                elif list_previous_pubissue[pos_issue+1][0][2] == '中旬、下旬':
                    end_day = 10  # or 10 如果有中旬
                else:
                    end_day = 15
            rendered_startday = datetime.date(int(year), int(start_month), int(start_day))
            rendered_endday = datetime.date(int(year), int(end_month), int(end_day))
            row = [list_previous_pubdate[pos_issue][0], str(rendered_startday), str(rendered_endday)]
            list_pubissue_daterange += [row]
            pos_issue = pos_issue + 1

    # Process the last issue
# 年 月 部分的处理
        year = list_previous_pubissue[pos_issue][0][0]
        month = list_previous_pubissue[pos_issue][0][1]
        month_items = month.split('、')
        if len(month_items) == 1:
            start_month = month_items[0]
            end_month = month_items[0]
        elif len(month_items) == 2:
            start_month = month_items[0]
            end_month = month_items[1]
# 对于 旬 的处理
        if list_previous_pubissue[pos_issue][0][2] == '没有旬':
            start_day = 1
            end_day = calendar.monthrange(int(year), int(end_month))[1]
        elif list_previous_pubissue[pos_issue][0][2] == '上旬':
            start_day = 1
            end_day = 10  # 暂时没有下一期来做判断，假设会有中旬
        elif list_previous_pubissue[pos_issue][0][2] == '上旬、中旬':
            start_day = 1
            end_day = 20
        elif list_previous_pubissue[pos_issue][0][2] == '中旬':
            start_day = 11
            end_day = 20
        elif list_previous_pubissue[pos_issue][0][2] == '中旬、下旬':
            start_day = 11
            end_day = calendar.monthrange(int(year), int(end_month))[1]
        elif list_previous_pubissue[pos_issue][0][2] == '下旬':
            if list_previous_pubissue[pos_issue][2][2] == '上旬、中旬': #检查上一期
                start_day = 21
                end_day = calendar.monthrange(int(year), int(end_month))[1]
            elif list_previous_pubissue[pos_issue][2][2] == '中旬':
                start_day = 21
                end_day = calendar.monthrange(int(year), int(end_month))[1]
            else:
                start_day = 16
                end_day = calendar.monthrange(int(year), int(end_month))[1]
        elif list_previous_pubissue[pos_issue][0][2] == '下旬、上旬':
            if list_previous_pubissue[pos_issue][2][2] == '上旬': #检查上一期
                start_day = 16
            else:
                start_day = 21
            end_day = 10  # 暂时没有下一期来做判断，假设会有中旬
        rendered_startday = datetime.date(int(year), int(start_month), int(start_day))
        rendered_endday = datetime.date(int(year), int(end_month), int(end_day))
        row = [list_previous_pubdate[pos_issue][0], str(rendered_startday), str(rendered_endday)]
        list_pubissue_daterange += [row]
        return list_pubissue_daterange

    def ReleaseInfo(self):
        reader = File()
        filepath = Path(r'C:\Users\VSurfacePro3\Desktop\Degree Classes\Trade University\CTAI\R_looklook\results\PubThreatricalRelease_info_allreleases.csv')
        all_releases = reader.open_to_list_of_list(filepath)
        return all_releases

    def Release_with_reg(self):
        allreleases = self.ReleaseInfo()
        allreleases = allreleases[1:len(allreleases)] # remove heading
        allreg = self.RegInfo()
        allreg = allreg[1:len(allreg)] # remove heading
        released_with_reg = []
        for release in allreleases:
   # match names, ignore names changes for now.
            release_reg_match = list(filter(lambda x:x[1] == release[2], allreg))
            if release_reg_match:
                released_with_reg += [release + release_reg_match]
        return released_with_reg

    def Release_with_unknownreg(self):
        allreleases = self.ReleaseInfo()
        allreleases = allreleases[1:len(allreleases)] # remove heading
        allreg = self.RegInfo()
        allreg = allreg[1:len(allreg)] # remove heading
        released_with_unknownreg = []
        for release in allreleases:
   # match names, ignore names changes for now.
            release_reg_match = list(filter(lambda x:x[1] == release[2], allreg))
            if not release_reg_match:
                released_with_unknownreg += [release]
        return released_with_unknownreg

    def Release_with_aireg(self):

        all_releases = self.ReleaseInfo()
        all_releases = allreleases[1:len(all_releases)] # remove heading
        all_reg = self.RegInfo()
        all_reg = allreg[1:len(all_reg)] # remove heading
        released_with_aireg = self.Release_with_reg()

        givener = Given()
        reg_to_release_given = givener.reg_to_release()
        for reg, release in reg_to_release_given.items():
            print(reg)
            print(release)
            corresponding_reg = list(filter(lambda x:x[0] == reg, allreg))
            corresponding_release = list(filter(lambda x:x[2] == release, all_releases))
            released_with_aireg += [corresponding_release[0] + corresponding_reg]

#            print(list(filter(lambda x:x[0] == reg, allreg)))
        return released_with_aireg

######################################################################
class Given(object):
    def __init__(self):
        if not self:
            raise ValueError

    def reg_to_release(self):
        reg_to_release ={u'影动备字[2017]第192号':u'新大头儿子和小头爸爸3俄罗斯奇遇记',
                         u'影剧备字[2014]第653号':u'幕后玩家',
                         u'影剧备字[2016]第341号':u'超时空同居',
                         u'影剧备字[2017]第8626号':u'你好，之华',
                         u'影剧备字[2017]第5534号':u'放学后联盟',
                         u'影剧备字[2018]第1594号':u'向爱而生',
                         u'影剧备字[2018]第1064号':u'菲凡记忆',
                         u'影剧备字[2016]第7518号':u'带我回家',
                         u'影合立字（2018）第035号':u'新喜剧之王',
                         u'影剧备字[2018]第521号':u'晃动乾坤',
                         u'影剧备字[2017]第1522号':u'神探蒲松龄',
                         u'影剧备字[2018]第3260号':u'皮秀英四告（淮海戏）',
                         u'影剧备字[2016]第5529号':u'相信·爱',
                         u'影剧备字[2018]第916号': u'神都危机',
                         u'影剧备字[2016]第1826号': u'迷妹罗曼史',
                         u'影剧备字[2015]第4674号': u'很高兴遇见·你',
                         u'影剧备字[2017]第3641号': u'侠路相逢',
                         u'影剧备字[2015]第4661号': u'最后一刻',
                         u'影剧备字[2017]第3973号': u'铁弓缘（京剧）',
                         u'影剧备字[2016]第8283号': u'幸福俏冤家',
                         u'影剧备字[2014]第3366号': u'天火行动',
                         u'影剧备字[2016]第884号': u'枣儿谣（蒲剧）',
                         u'影剧备字[2017]第1677号': u'少女宿舍',
                         u'影剧备字[2018]第4315号': u'我们的爱情',
                         u'影剧备字[2017]第4120号': u'我在社区当片儿警',
                         u'影剧备字[2017]第2845号': u'秦·火',
                         u'影剧备字[2017]第6168号': u'乐乐不可知',
                         u'影剧备字[2017]第3741号': u'执手当年',
                         u'影剧备字[2017]第8491号': u'西河十八弯'}
        return reg_to_release
######################################################################
class Extract(object):
    def __init__(self):
        if not self:
            raise ValueError

    def columnfromlistoflist(self, listoflist, pos_col):
        column = []
        for eachlist in listoflist:
            column.append(eachlist[pos_col])
        return column
######################################################################
class Find(object):

    def __init__(self):
        if not self:
            raise ValueError

    def PreviousPubDate(self, current_pub_title, list_previouspubdate):
        pos_title = 0
        previous_pub_date = ''
        while pos_title < len(list_previouspubdate):
            if current_pub_title == list_previouspubdate[pos_title][0]:
                previous_pub_date = list_previouspubdate[pos_title][3]
                break
            else:
                pos_title = pos_title + 1
        return previous_pub_date

    def DateRange(self, string_title, list_pubissue_daterange, pos_title=0, pos_startdate=1, pos_enddate=2):
        for pubissue in list_pubissue_daterange:
            if pubissue[pos_title] == string_title:
                row = [pubissue[pos_startdate], pubissue[pos_enddate]]
                return row
                break
######################################################################
class Parse(object):

    def __init__(self):
        if not self:
            raise ValueError

    def PubDate(self, string_regpubdate):
#        sample = '2019-03-11 17:21'
        dt = datetime.datetime.strptime(string_regpubdate, "%Y-%m-%d %H:%M")
        return dt

    def IssueDate(self, string_issuedate):
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
#####################################################################
class Interpret(object):
    def __init__(self):
        if not self:
            raise ValueError

    def summary_bysubmityear(self, string_filmtype, list_parsed_regid_pubtitle):
# 按照提交备案的年做年度分析，需要输入种类
        list_filtered = list(filter(lambda x:x[1] == string_filmtype, list_parsed_regid_pubtitle))
        list_toint = list(map(lambda x:[x[0], x[1], int(x[2]),int(x[3]), x[4], x[5]], list_filtered))
        year_tosearch = list(range(2009,datetime.datetime.now().year+1,1))
        summary_bysubmityear = []
        for year in year_tosearch:
            list_by_year = list(filter(lambda x:x[2] == year, list_toint))
            if list_by_year:
                list_by_year_sorted = sorted(list_by_year, key=itemgetter(3))
                total_reginyear_est = list_by_year_sorted[len(list_by_year_sorted)-1][3] # 当年提交 备案号 中之 序列号 的最大值， 预估某年中一共提交了多少个备案
                total_passed_in_regyear = len(list_by_year) # 某一年 提交的 备案 已获准备案的
                rate_pass_est = total_passed_in_regyear / total_reginyear_est # 某一年 备案的 故事片的 通过率
                summary_bysubmityear += [[year, total_reginyear_est, total_passed_in_regyear, rate_pass_est]]
            else:
                summary_bysubmityear += [[year, 0, 0, None]]
        return summary_bysubmityear

    def summary_bysubmityear_jointypes(self, summary_bysubmityear1, summary_bysubmityear2):
        return list(map(lambda x,y:[x[0], x[1]+y[1], x[2]+y[2], (x[2]+y[2])/(x[1]+y[1])],
                     summary_bysubmityear1, summary_bysubmityear2))


    def summary_byissue(self, string_filmtype, string_issuedate, string_previous_issuedate, list_parsed_regid_pubtitle):
        parser = Parse()
# 按照备案公示批次做批次分析 ，需要输入 （1）种类 （2）批次日期
        list_filtered = list(filter(lambda x:x[4] == string_issuedate and x[1] == string_filmtype, list_parsed_regid_pubtitle))
        year_tosearch = list(range(2009,parser.IssueDate(string_issuedate).year))
        if list_filtered:
            list_toint = list(map(lambda x:[x[0], x[1], int(x[2]),int(x[3]), x[4], x[5]], list_filtered))
            list_sorted = sorted(list_toint, key=itemgetter(2,3))
            total_passed_in_issuetime = len(list_sorted)
            earliest_reg_passed = list_sorted[0]
            latest_reg_passed = list_sorted[len(list_sorted)-1]
            earliest_reg_passed_thisyear = list(filter(lambda x:x[2] == parser.IssueDate(string_issuedate).year, list_sorted))
            if earliest_reg_passed_thisyear:
                earliest_reg_passed_thisyear = list(filter(lambda x:x[2] == parser.IssueDate(string_issuedate).year, list_sorted))[0]
                latest_reg_passed_thisyear = list(filter(lambda x:x[2] == parser.IssueDate(string_issuedate).year, list_sorted))[-1]
            else:
               earliest_reg_passed_thisyear = None
               latest_reg_passed_thisyear = None
# count number of films from previous year
            items_from_prior_year = {}
            total_passed_from_previous_years = 0
            for year in year_tosearch:
                year_of_prior_year = year
                number_passed_from_prior_year = len(list(filter(lambda x:x[2]==year, list_sorted)))
                items_from_prior_year.update({year_of_prior_year:number_passed_from_prior_year})
                total_passed_from_previous_years = total_passed_from_previous_years + number_passed_from_prior_year
        else:
            total_passed_in_issuetime = 0
            earliest_reg_passed = None
            latest_reg_passed = None
            earliest_reg_passed_thisyear = None
            latest_reg_passed_thisyear = None
            number_passed_from_prior_year = 0
            items_from_prior_year = 0
            total_passed_from_previous_years = 0

        list_filtered_previous = list(filter(lambda x:x[4] == string_previous_issuedate and x[1] == string_filmtype, list_parsed_regid_pubtitle))
        if list_filtered_previous:
            list_toint_previous = list(map(lambda x:[x[0], x[1], int(x[2]),int(x[3]), x[4], x[5]], list_filtered_previous))
            list_sorted_previous = sorted(list_toint_previous, key=itemgetter(2,3))
            earliest_reg_passed_thisyear_previous = list(filter(lambda x:x[2] == parser.IssueDate(string_previous_issuedate).year, list_sorted_previous))
            if earliest_reg_passed_thisyear_previous:
                earliest_reg_passed_thisyear_previous = list(filter(lambda x:x[2] == parser.IssueDate(string_previous_issuedate).year, list_sorted_previous))[0]
            else:
                earliest_reg_passed_thisyear_previous = None
            latest_reg_passed_previous = list_sorted_previous[len(list_sorted_previous)-1]

        else:
            earliest_reg_passed_thisyear_previous = None
            latest_reg_passed_previous = None



# Max reg_thisissue - max reg_previousmonth + processed from previous years
        if string_issuedate == '2011-01-16':
            if latest_reg_passed:
                total_cases_processed_duringissuetime_est = latest_reg_passed[3] + total_passed_from_previous_years
            else:
                total_cases_processed_duringissuetime_est = 0
        elif parser.IssueDate(string_issuedate).month == 1 and parser.IssueDate(string_issuedate).day == 1:
            if latest_reg_passed:
                total_cases_processed_duringissuetime_est = latest_reg_passed[3] + total_passed_from_previous_years
            else:
                total_cases_processed_duringissuetime_est = total_passed_from_previous_years
        else:
            if latest_reg_passed_thisyear:
                total_cases_processed_duringissuetime_est = (latest_reg_passed_thisyear[3]
                            / ((parser.IssueDate(latest_reg_passed_thisyear[5])
                               - datetime.datetime(parser.IssueDate(latest_reg_passed_thisyear[5]).year, 1, 1)).days)
                            * ((parser.IssueDate(latest_reg_passed_thisyear[5])
                               - parser.IssueDate(latest_reg_passed_thisyear[4])).days)
                            + total_passed_from_previous_years)

                if total_cases_processed_duringissuetime_est < total_passed_in_issuetime:
                    total_cases_processed_duringissuetime_est = total_passed_in_issuetime # 目前总数有估少，可以试下除以年分类通过率
            else:
                total_cases_processed_duringissuetime_est = total_passed_from_previous_years
            # 今年的最大备案号序号 / 今年过了多少天 * 当期的天数 + 通过的往年的备案
        if total_cases_processed_duringissuetime_est == 0:
            passrate_est = 0
        else:
            passrate_est = total_passed_in_issuetime / total_cases_processed_duringissuetime_est
        row = [string_issuedate, # 本期 备案公示
                string_filmtype, # 影片类型
                round(total_cases_processed_duringissuetime_est), # 当期收到 备案 量 （滚动预估）
                total_passed_in_issuetime,  # 当期 通过量
                round(passrate_est,4), # 本期 备案完成率
                earliest_reg_passed_thisyear_previous, # 上一期备案公示 通过的 本年度最早 备案公示编号
                latest_reg_passed_previous, # 上一期备案公示 通过的 最大 备案编号
                earliest_reg_passed, # 本期 通过的 最早 备案公示编号
                earliest_reg_passed_thisyear, # 本期 通过的 本年度最早 备案公示编号
                latest_reg_passed_thisyear, # 本期 通过的 本年度最大 备案编号
                latest_reg_passed, # 本期 通过的 最大 备案编号
                number_passed_from_prior_year, # 本期 处理完结的 之前年份提交的备案的 总量
                items_from_prior_year] #本期 处理完结的 之前年份提交的备案的 分布
        return row
#####################################################################
class View(object):

    def __init__(self):
        if not self:
            raise ValueError

    def regsummary_by_submityear(self, str_filmtype, heading=False):
        # 加载函数
        getter = Get()
        parser = Parse()
        finder = Find()
        interpreter = Interpret()
        #获取 目前所有 备案信息， 去掉标题行
        all_reg = getter.RegInfo()
        all_reg = all_reg[1:len(all_reg)]
        # 获取每个公示批次所对应的日期范围
        list_pubissue_daterange = getter.List_PubIssue_DateRange()

        all_release = getter.ReleaseInfo()

        list_parsed_regid_pubtitle = []
        index = 0
        while index < len(all_reg):
            row = []
            row.append(all_reg[index][1]) #片名
            row += parser.RegID(all_reg[index][0]) #备案号解读
            row += finder.DateRange(all_reg[index][8], list_pubissue_daterange, 0, 1, 2) # Issue date range
            list_parsed_regid_pubtitle += [row]
            index = index + 1

        summary_by_submityear = interpreter.summary_bysubmityear(str_filmtype, list_parsed_regid_pubtitle)
        if heading:
            heading = ['提交备案之年','该年提交的备案总量【估】', '该年提交的备案获通过的数量','通过率【估】']
            summary_by_submityear = [heading] + summary_by_submityear
        return summary_by_submityear

    def regsummary_by_issue(self, heading=False):
        # 加载函数
        getter = Get()
        parser = Parse()
        finder = Find()
        interpreter = Interpret()

        # 获取备案信息列表
        all_reg = getter.RegInfo()
        all_reg = all_reg[1:len(all_reg)]

        # 获取 公示批次列表 及 其 所对应的日期
        list_pubissue_daterange = getter.List_PubIssue_DateRange()

        # 获取 公映公示信息 列表
        all_releases = getter.ReleaseInfo()

        # 对 备案号进行 解析
        list_parsed_regid_pubtitle = []
        index = 0
        while index < len(all_reg):
            row = []
            row += [all_reg[index][1]] #片名
            row += parser.RegID(all_reg[index][0]) #备案号解读
            row += finder.DateRange(all_reg[index][8], list_pubissue_daterange) # Issue date range
            index = index + 1
            list_parsed_regid_pubtitle += [row]

        # 故事片 按备案批次 的 总结表
        summary_by_pubissue_drama = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_drama += [interpreter.summary_byissue('故事片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 合拍片 按备案批次 的 总结表
        summary_by_pubissue_coproduction = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_coproduction += [interpreter.summary_byissue('合拍片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 协拍片 按备案批次 的 总结表
        summary_by_pubissue_supporting = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_supporting += [interpreter.summary_byissue('协拍片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 纪录片 按备案批次 的 总结表
        summary_by_pubissue_documentary = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_documentary += [interpreter.summary_byissue('纪录片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 特种片 按备案批次 的 总结表
        summary_by_pubissue_special = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_special += [interpreter.summary_byissue('特种片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 动画片 按备案批次 的 总结表
        summary_by_pubissue_animation = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_animation += [interpreter.summary_byissue('动画片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 科教片 按备案批次 的 总结表
        summary_by_pubissue_science = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_science += [interpreter.summary_byissue('科教片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        # 重大历史题材片 按备案批次 的 总结表
        summary_by_pubissue_significance = []
        pos_issue = 0
        while pos_issue < len(list_pubissue_daterange):
            summary_by_pubissue_significance += [interpreter.summary_byissue('重大历史题材片',
                                          list_pubissue_daterange[pos_issue][1], list_pubissue_daterange[pos_issue-1][1],
                                          list_parsed_regid_pubtitle)]
            pos_issue = pos_issue + 1

        summary_by_pubissue_alltype = (summary_by_pubissue_drama
                                       + summary_by_pubissue_coproduction
                                       + summary_by_pubissue_supporting
                                       + summary_by_pubissue_documentary
                                       + summary_by_pubissue_special
                                       + summary_by_pubissue_animation
                                       + summary_by_pubissue_science
                                       + summary_by_pubissue_significance)
        if heading:
            heading = ['本期公示期间', '影片类型', '本期受理备案量【估】',
                       '本期通过量【估】', '本期滚动通过率【估】',
                       '上期通过的本年最早备案号','上期通过的最大备案号',
                       '本期通过的最早备案号', '本期通过的本年最早备案号',
                       '本期通过的本年最大备案号', '本期通过的最大备案号',
                       '本期通过的过去年份的备案总量', '本期通过的过去年份的备案分布']
            summary_by_pubissue_alltype = [heading] + summary_by_pubissue_alltype

        return summary_by_pubissue_alltype

    def bytimeline(self):
        getter = Get()
        parser = Parse()
        finder = Find()

        allreg = getter.RegInfo()
        allreg = allreg[1:len(allreg)]
        list_pubIssue_daterange = getter.List_PubIssue_DateRange()

        list_parsed_pubtitle = []

        index = 0
#        row_heading = ['片名', '片种', '备案年', '备案编号','公示年','公示月','公示月批次','公示日期','上期公示日期']
#        while index < len(allreg):
        while index < 5:
            row = []
            row.append(allreg[index][1]) #片名
            row += parser.RegID(allreg[index][0]) #备案号解读
            row += finder.DateRange(allreg[index][8], list_pubIssue_daterange, 0, 1, 2)
#            row += parser.PubTitle(allreg[index][8]) #公示文件名解读
            row += [str(parser.PubDate(allreg[index][7]))] #公示日期
#            row += [finder.PreviousPubDate(allreg[index][8], list_previouspubdate)] #前一期公示日期
            index = index + 1
            list_parsed_pubtitle += [row]
        return list_parsed_pubtitle
######################################################################
