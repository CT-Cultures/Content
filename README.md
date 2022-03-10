# ContentAI

## ContentAI provides datasets and tools to perform data analysis on films, tv and web contents. 
Currently, this packages focus on production analysis on films an television records from China.
We will be working on expanding global coverage.

### (1) Datasets- ContentAI currently supports and maintains the following datasets：
#### ChinaFilm - China Film Administration - 中国国家电影局
    
    #update film registration records from ChinaFilm
    python run ./sources/ChinaFilm/update_registration.py
   
    #update film release permit records from ChinaFilm
    python run ./sources/ChinaFilm/update_release.py
    
    #filepath to ChinaFilm registration records
    fp_ChinaFilm_reg = './sources/ChinaFilm/records/contents_of_registrations.json'
    
    #filepath to ChinaFilm release records
    fp_ChinaFilm_release = './sources/ChinaFilm/records/contents_of_releases.json'
    
    #import to pandas
    import pandas as pd
    filepath = './sources/ChinaFilm/records/contents_of_registrations.json'
    df = pd.read_json(filepath)
        
#### NRTA - National Radio and Television Administration - 中国国家广电总局

     #update NRTA
     python run ./sources/NRTA/update_registration.py
     
     #备案公示 数据集路径
     fp_NRTA_reg = './sources/NRTA/contents_of_registrations.json'
  
#### ZGDYPW - China Moview Database - 中国电影数据信息网 

     #update ZGDYPW new release records
     python run ./update_newrelease.py
     
     #file path to ZGDYPW new release records
     fp_ZGDYPW_intheater_preview = './sources/zgdypw/contents_of_releases.py'

#### A note on the differences between ChinaFilm's release records and ZGDYPW's new release records
 The films in China Film's release records indicate that the films have obtained 
 release permits, thus become eligible for release in theaters. Not all films
 with a release permits play in theaters. 
 
 The ZGDYPW's new release records track the latest films with an on-screen date,
 this is a good indicator that the film will actually play in theaters. In the future, 
 we plan to cross check information with dcp keys. Each theatrical release format 
 (2D, 3D, iMAX, etc) will have an unique access key for corresponding DCP copies, so that
 theaters can download to unlock playback. Having a key further strengthens
 the probability of a film actually hits the theater.
