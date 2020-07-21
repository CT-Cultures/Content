# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 01:38:32 2020

@author: VSurfacePro3
"""

#%% Load Libraries
import pandas as pd
import numpy as np

import sys
#sys.path.append('../../../sources')
sys.path.insert(0, 'C:/Users/VSurfacePro3/Documents/GitHub/Content/sources')

from dy_cn.dy_Registration import Registration
#%%
dyreg = Registration()

records = dyreg.update_records()

"""

{} 公示了{}的备案立项， 距离上一次公示已过去了{}天。
从本次通公示的项目来看，推测为{}前提交的备案申请，在此之后提出的申请如果还没有公示不必过于担心，
【毕竟电影院何时恢复营业还是未知数】, 每部电影都有自己的际遇，一切都有最好的安排。

本期公示的备案中，有{}部{}、{}部{}，其中我们特别关注的有：

{}， 因为
{}， 因为

头部影视公司新增的备案有 {}、{}、{}。

"""