# ContentAI

## ContentAI gathers records from the various sources for registration, permit and release information on film, TV and web projects and saves the records to json with after some cleanup.

### (1) Datasets- ContentAI currently tracks updates from the following sources：
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
     
## License
[LICENSE](LICENSE.md)
