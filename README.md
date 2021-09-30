# Content

##This Project tracks film, TV and Web Series Registration and Release Records.

##(1) Data Sources include:
  - ChinaFilm 中国国家电影局- film registration, film release permit
  - NRTA 中国国家广电总局 TV registration
  - IMDB
  - Douban 豆瓣
  - Maoyan 猫眼
  - Endata 艺恩智库
  - Taopiaopiao 淘票票

##Sample Usage: python rum ChinaFilm/update_registrations.py
                python run ChinaFilm/update_releases.py
                python run NRTA/update_records.py
Alternatively, One can use the corresponding jupyter notebooks to update and review records.


(2) Tools include:
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

###Screenplay Module had spun off to become a standalone repository， it offers screenplay formatting, translation and synopsis generation capabilities. Screenplay现已成为独立的Repo，提供剧本格式转换，翻译及梗概生成工具。

###Article Module had spun off to become a standalone repository, it create analytical reports from the content database.
