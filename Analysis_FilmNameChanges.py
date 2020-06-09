# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 01:50:29 2019

@author: VSurfacePro3
"""
# from Global
import rpy2
from rpy2.robjects.packages import importr
# import R's "base" package
base = importr('base')

# import R's "utils" package
utils = importr('utils')
from pathlib import Path

import numpy as np
import matplotlib
from matplotlib import pyplot
import math
import statistics

# from local
from IO_Storage import File
#%%
rb_wbo_100 = list(filter(lambda x:int(x[4]) >= 100, rb_wbo))
rf_wbo_100 = list(filter(lambda x:int(x[4]) >= 100, rf_wbo))
rkw_wbo_100 = list(filter(lambda x:int(x[4]) >= 100, rkw_wbo))
rsig_wbo_100 = list(filter(lambda x:int(x[4]) >= 100, rsig_wbo))
rwonamechange_wbo_100 = list(filter(lambda x:int(x[4]) >= 100, rwonamechange_wbo))
#%%
print(rpy2.__version__)
pi = rpy2.robjects.r['pi']

rwbo = list(map(lambda x:int(x[4]), rwonamechange_wbo_100))
mean_rwbo = statistics.mean(rwbo)
stdev_rwbo = statistics.stdev(rwbo)

rsigbo = list(map(lambda x:int(x[4]), rsig_wbo_100))
rsigbo_sorted = list(sorted(rsigbo))
mean_rsigbo = statistics.mean(rsigbo)
stdev_rsigbo = statistics.stdev(rsigbo)
pyplot.boxplot(rsigbo, showmeans=True, showfliers=True)


rfbo = list(map(lambda x:int(x[4]), rf_wbo_100))
mean_rfbo = statistics.mean(rfbo)
stdev_rfbo = statistics.stdev(rfbo)

rbbo = list(map(lambda x:int(x[4]), rb_wbo_100))
mean_rbbo = statistics.mean(rbbo)
stdev_rbbo = statistics.stdev(rbbo)

rkbo = list(map(lambda x:int(x[4]), rkw_wbo_100))
mean_rkwbo = statistics.mean(rkwbo)
stdev_rkwbo = statistics.stdev(rkwbo)

rchbo = rsigbo + rfbo + rbbo + rkwbo
mean_rchbo = statistics.mean(rchbo)
stdev_rchbo = statistics.stdev(rchbo)


plotter = pyplot.boxplot([rwbo, rsigbo, rbbo, rfbo, rkwbo],
                         showbox=True)



plotter = pyplot.boxplot([rwbo, rchbo],
                         showbox=True)

#%%
def reject_outliers(data, m=2):
  return data[abs(data - np.mean(data)) < m * np.std(data)]

#%% Load data
loader = File()
dir_root = 'C:\\Users\\VSurfacePro3\\Desktop\\Degree Classes\\Trade University\\CTAI\\R_looklook\\results'
path_project = 'tostudy\\Effects of Name Change'

filename = 'rf_wbo'
filepath = dir_root + "\\" + path_project + "\\" + filename + ".csv"
rf_wbo = loader.open_to_list_of_list(Path(filepath))

filename = 'rb_wbo'
filepath = dir_root + "\\" + path_project + "\\" + filename + ".csv"
rb_wbo = loader.open_to_list_of_list(Path(filepath))

filename = 'rkw_wbo'
filepath = dir_root + "\\" + path_project + "\\" + filename + ".csv"
rkw_wbo = loader.open_to_list_of_list(Path(filepath))

filename = 'rsig_wbo'
filepath = dir_root + "\\" + path_project + "\\" + filename + ".csv"
rsig_wbo = loader.open_to_list_of_list(Path(filepath))

filename = 'r_wonamechange_wbo'
filepath = dir_root + "\\" + path_project + "\\" + filename + ".csv"
r_wonamechange_wbo = loader.open_to_list_of_list(Path(filepath))

del dir_root
del filename
del filepath
del path_project
#%%