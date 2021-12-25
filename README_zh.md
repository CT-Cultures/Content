# ContentAI 慷田AI

## ContentAI 为影视数据提供了基础工具，目前主要针对中国大陆的影视数据进行分析，并逐渐引入世界影视数据。

### (1) 数据集 - ContentAI 目前支持 收集、维护下列数据集，数据集：
#### 中国国家电影局 ChinaFilm
    
    #更新 备案公示 数据集
    python run ./sources/ChinaFilm/update_registration.py
   
    #更新 公映许可公示 数据集
    python run ./sources/ChinaFilm/update_release.py
    
    #备案公示 数据集路径
    fp_ChinaFilm_reg = './sources/ChinaFilm/records/contents_of_registrations.json'
    
    #公映许可 数据集路径
    fp_ChinaFilm_release = './sources/ChinaFilm/records/contents_of_releases.json'
    
    #Pandas 导入示例
    import pandas as pd
    filepath = './sources/ChinaFilm/records/contents_of_registrations.json'
    df = pd.read_json(filepath)
        
#### 中国国家广电总局 NRTA

     #更新 备案公示 数据集
     python run ./sources/NRTA/update_registration.py
     
     #备案公示 数据集路径
     fp_NRTA_reg = './sources/NRTA/contents_of_registrations.json'
  
#### 中国电影数据信息网 ZGDYPW

     #更新 新片上映预告 数据集
     python run ./update_intheater_preview.py
     #新片上映预告 数据集路径
     
     fp_ZGDYPW_intheater_preview = './sources/zgdypw/update_intheater_preview.py'

### (2) 信息搜索工具
####IMDB
####百度百科 Baidu Baike 
####豆瓣 Douban 
####猫眼 Maoyan 
####艺恩智库 Endata 
####淘票票 Taopiaopiao 

## (2) 工具 Tools:
### 影片类型识别器 - 输入影片梗概，自动判断影片的类型
          使用示例 from tools
### 影片年代识别器 - 输入影片梗概，自动判断影片的年代
### 主角识别器 

### 关键词提取
    - abstractive title prediction 生成式片名预测
    - extractive title prediction 抽取式片名预测
    - TF-IDF keyword extraction 逆文本词频关键词提取
