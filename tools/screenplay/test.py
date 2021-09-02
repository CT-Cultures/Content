# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:01:10 2021

@author: VXhpUS
"""

import Screenplay
#%%

scp = Screenplay.Screenplay()
#%%
fp = 'F:/Github/Content/tools/screenplay/input/合并剧本word.docx'
fp = 'F:/Github/Content/tools/screenplay/output/wanglai.xml'
fp = 'input/Avatar (2009 film)_script.txt'


#%%
avatar = scp.read.text(fp)
print(avatar)