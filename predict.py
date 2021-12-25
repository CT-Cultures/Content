# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 22:11:14 2021
@author: Herais
"""
import sys
import os
import pandas as pd
import numpy as np
import re
import transformers
from collections import Counter
import torch
import gdown

#%% id_main_character(ls_summary)
import jieba.analyse
import jieba
import jieba.posseg as pseg
tfidf = jieba.analyse.extract_tags
textrank = jieba.analyse.textrank
jieba.enable_paddle() #启动paddle模式。 0.40版之后开始支持，早期版本不支持

from transformers import BertTokenizer, BartForConditionalGeneration

#%Predict Title%
def predict_title(ls_summary,
                  path_model:str="default",
                  batch_size:int=8,
                 ):
    
    # assign device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Instantiate tokenizer and model
    checkpoint = path_model
    if checkpoint == "default":
       checkpoint = "tools/models/model_predict_title"
    tokenizer = BertTokenizer.from_pretrained(checkpoint)
    model = BartForConditionalGeneration.from_pretrained(checkpoint).to(device)
    model.eval()
    
    i = 0
    L = len(ls_summary)
    predictions = []
    while i < L:
      inputs = tokenizer(ls_summary[i:i+batch_size],
                         padding=True,
                         #max_length=512, 
                         truncation=True, 
                         return_tensors='pt')
      inputs.to(device)
      
      summary_ids = model.generate(input_ids=inputs['input_ids'],
                                num_beams=4,
                                min_length=0,
                                max_length=32
                                )
      
      ret = [tokenizer.decode(g, 
                              skip_specical_tokens=True, 
                              clean_up_tokenization_spaces=True
                              ) 
             for g in summary_ids
            ]
      
      predictions.extend(ret)
      i += batch_size
      
    def remove_specials(x):
        x = re.sub(' ', '', x)
        x = re.sub('\[CLS\]', '', x)
        x = re.sub('\[PAD\]', '', x)
        x = re.sub('\[SEP\]', '', x)
        return x
    
    predictions = [remove_specials(p) for p in predictions]
    return predictions

#%Predict Genre%
from transformers import BertTokenizer, BertForSequenceClassification

def predict_genre(ls_summary,
                  path_model:str="default",
                  batch_size:int=8,
                 ):
    
    # Define Labels
    label2id_genre= {'传奇': 0, '传记': 1, '其它': 2, '军旅': 3, '农村': 4, '宫廷': 5,  
                  '武打': 6, '涉案': 7, '神话': 8, '科幻': 9, '都市': 10, '青少': 11,
                  '革命': 12}
    id2label_genre = {}
    for k, v in label2id_genre.items(): id2label_genre[v] = k
    
    # Genre Classifier
    N_LABELS = len(id2label_genre)
    ID2LABEL = id2label_genre
    LABEL2ID = label2id_genre
    
    # assign device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    checkpoint = path_model
    if checkpoint == "default":
        checkpoint = "tools/models/model_predict_genre"   
    tokenizer = BertTokenizer.from_pretrained(checkpoint)
    model = BertForSequenceClassification.from_pretrained(
      checkpoint,
      num_labels=N_LABELS,
      problem_type="multi_label_classification",
      id2label=ID2LABEL,
      label2id=LABEL2ID,  
    ).to(device)
    
    model.eval() # set model to eval mode for faster prediction
    
    i = 0
    softmax = torch.nn.Softmax(dim=-1)
    L = len(ls_summary)
    predictions = []    
    while i < L:
      batch_test = tokenizer(ls_summary[i:i+batch_size],
                             padding=True,
                             max_length=512, 
                             truncation=True, 
                             return_tensors='pt'
                            )
      batch_test.to(device)
      batch_outputs = model(**batch_test)
      batch_logtis = batch_outputs.logits
      batch_softmax = softmax(batch_logtis)
      batch_results = torch.argmax(batch_softmax, dim=1).cpu().numpy()
      predictions.extend(list(batch_results))
      i += batch_size
    
    predictions = [id2label_genre[p] for p in predictions]
    return predictions

#%Predict Time Period%
from transformers import BertTokenizer, BertForSequenceClassification

def predict_time(ls_summary,
                 path_model:str="default",
                 batch_size:int=8,
                 ):
    
    # Define Labels
    label2id_time = {'古代': 0, '当代': 1, '现代': 2, '近代': 3}
    id2label_time = {}
    for k, v in label2id_time.items(): id2label_time[v] = k
        
    # Genre Classifier
    N_LABELS = len(id2label_time)
    ID2LABEL = id2label_time
    LABEL2ID = label2id_time
    
    # assign device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    checkpoint = path_model
    if checkpoint == "default":
        checkpoint = "tools/models/model_predict_timeperiod" 
    
    tokenizer = BertTokenizer.from_pretrained(checkpoint)
    model = BertForSequenceClassification.from_pretrained(
      checkpoint,
      num_labels=N_LABELS,
      problem_type="multi_label_classification",
      id2label=ID2LABEL,
      label2id=LABEL2ID,  
    ).to(device)
    model.eval() # set model to eval mode for faster prediction
    
    i = 0
    softmax = torch.nn.Softmax(dim=-1)
    L = len(ls_summary)
    predictions = []    
    while i < L:
      batch_test = tokenizer(ls_summary[i:i+batch_size],
                             padding=True,
                             max_length=512, 
                             truncation=True, 
                             return_tensors='pt'
                            )
      batch_test.to(device)
      batch_outputs = model(**batch_test)
      batch_logtis = batch_outputs.logits
      batch_softmax = softmax(batch_logtis)
      batch_results = torch.argmax(batch_softmax, dim=1).cpu().numpy()
      predictions.extend(list(batch_results))
      i += batch_size
    
    predictions = [id2label_time[p] for p in predictions]
    return predictions

#%extract_keywords%
def extract_keywords(x, topK=10):
  return textrank(x, topK=10)

#%Identify Characters%
def identify_characters(x: pd.Series):
  # 识别主要角色
  words = pseg.cut(x, use_paddle=True)
  ls_PER = []
  for word, flag in words:
    if flag == 'PER':
      word = word.strip('[\s,，。、“”？；]')
      ls_PER.append(word)
  ls_PER = list(set(ls_PER))

  ls_PER1 = ls_PER.copy()
  ls_PER = []
  while ls_PER1:
    PER =  ls_PER1.pop(0)
    ls_tmp = re.split('[\s,，。、“”？；]', PER)
    ls_PER.extend(ls_tmp)

  ls_PER = list(set(ls_PER)) 
  ls_PER = [PER for PER in ls_PER if len(PER) > 1]
  ls_PER_sorted = sorted(ls_PER, reverse=False, key=lambda x: len(x))

  ans = []
  while ls_PER_sorted:
    PER = ls_PER_sorted.pop(0)
    i = 0
    while i < len(ls_PER_sorted):
      if re.search(PER, ls_PER_sorted[i]):
        ls_PER_sorted.pop(i)
        ans.append(PER)
      i += 1
    if PER not in ans:
      ans.append(PER)

  return ans