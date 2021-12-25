# Content

## This Project tracks Film, TV and Web Series Registration and Release Records
from China, and is capable of performing related searches on various content database
sites.

## (1) 数据来源:
  - 中国国家电影局 ChinaFilm
        获得最备案数据：python run NRTA/update_registration.py
        获得公映许可数据：python run ChinaFilm/update_release.py
        
  - NRTA 中国国家广电总局 TV registration
        python run NRTA/update_registration.py
  
  - ZGDYPW 中国电影数据信息网
  - IMDB
  - Baidu Baike 百度百科
  - Douban 豆瓣
  - Maoyan 猫眼
  - Endata 艺恩智库
  - Taopiaopiao 淘票票

## Sample Usage: python rum ChinaFilm/update_registrations.py
                python run ChinaFilm/update_releases.py
                python run NRTA/update_records.py
Alternatively, One can use the corresponding jupyter notebooks to update and review records.


## (2) Tools include:
  - Genre classification from short synopsis 类型识别
  - Time Period classification from short synopsis 年代识别
  - NER 
    - Character Recognition from synopsis 主角识别
  - Key phrase/word idenfication 关键词内容提取
    - abstractive title prediction 生成式片名预测
    - extractive title prediction 抽取式片名预测
    - TF-IDF keyword extraction 逆文本词频关键词提取
  - WIP
    - Story Progression Similarity Comparison 用梗概检索类似的故事

### Screenplay Module had spun off to become a standalone repository， it offers screenplay formatting, translation and synopsis generation capabilities. Screenplay现已成为独立的Repo，提供剧本格式转换，翻译及梗概生成工具。

### Article Module had spun off to become a standalone repository, it create analytical reports from the content database.
