# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 23:49:32 2021

@author: VXhpUS
"""

import os
import pandas as pd

import gdown
#import torch
gdown.__version__
#%%
checkpoint = "default"
if checkpoint == "default":
    checkpoint = "./tools/models/model_predict_title"
    if not os.path.exists(checkpoint):
        url ='https://drive.google.com/file/d/1toeoC7OHmjSq8qAL_UBhe8YZb4vDnvOM'
        gdown.download(url, "./tools/models", quiet=True)
