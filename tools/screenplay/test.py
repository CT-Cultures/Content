# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 15:01:10 2021

@author: VXhpUS
"""
import re
import Screenplay
#%%

scp = Screenplay.Screenplay()
#%%
fp = 'F:/Github/Content/tools/screenplay/input/合并剧本word.docx'
fp = 'F:/Github/Content/tools/screenplay/output/wanglai.xml'
fp = 'input/Avatar (2009 film)_script.txt'


#%%
dfsc = scp.read.text(fp)

#%%
idx_sh = dfsc[dfsc['Grp'] == 'H'].index
#%%
dfsc.loc[dfsc.index.isin(idx_sh), 'Element']
#%%

dfsc.loc[dfsc.index.isin(idx_sh), 'IE'] = \
    dfsc.loc[dfsc.index.isin(idx_sh), 'Element'].str.extract(
        '({})'.format('|'.join(pat_sh)), expand=False)
#%%

def extract_location(x):
    if x['Element']:
        location = x['Element']
    else: return ''
    if x['IE']:
        location = re.sub(str(x['IE']), '', location)
    if x['Time']:
        location = re.sub(str(x['Time']), '', location)
        
    location = re.sub('[-——\.,]+', '', location)
    return location.strip()
    

dfsc.loc[dfsc.index.isin(idx_sh), 'Location'] = dfsc.loc[dfsc.index.isin(idx_sh), :].apply(lambda x: extract_location(x), axis=1)

#%%

test = dftmp[:10].apply(scp.translate.Baidu, lang_from='en', lang_to='zh')
#%%
scp.translate.Baidu('apple', 'en', 'zh')
#%%
'|'.join(pat_sh)