# ContentAI 慷田AI

## ContentAI 为影视数据提供了基础工具，目前主要针对中国大陆的影视数据进行分析，并逐渐引入世界影视数据。

### (1) 数据集 - ContentAI 目前支持 收集、维护下列数据集，数据集：
  - 中国国家电影局 ChinaFilm
        -- 更新 备案公示 数据集： python run ./sources/ChinaFilm/update_registration.py
        -- 更新 公映许可公示 数据集：python run ./sources/ChinaFilm/update_release.py
        -- 备案公示 数据集路径：./sources/ChinaFilm/records/contents_of_registrations.json
        -- 公映许可 数据集路径：./sources/ChinaFilm/records/contents_of_releases.json
        -- Pandas 导入示例：df = pd.read_json('{文件路径}')
        
  - 中国国家广电总局 NRTA
        更新 备案公示 数据集： python run ./sources/NRTA/update_registration.py
        备案公示 数据集路径： ./sources/NRTA/contents_of_registrations.json
  
  - 中国电影数据信息网 ZGDYPW
        更新 新片上映预告 数据集：python run ./update_intheater_preview.py
        新片上映预告 数据集路径： ./sources/zgdypw/update_intheater_preview.py

### Pandas 导入示例
                df = pd.read_json('{文件路径}')


### (2) 信息搜索工具
  - IMDB
  - 百度百科 Baidu Baike 
  - 豆瓣 Douban 
  - 猫眼 Maoyan 
  - 艺恩智库 Endata 
  - 淘票票 Taopiaopiao 




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
