# Content

This Project tracks film, TV and Web Series Registration and Release Records.

(1) Currently supported Data Sources
  - ChinaFilm, including film registration and release permit records.
  - NRTA, including TV registration records, will gradually include
  
  Sample Usage: python rum ChinaFilm/update_registrations.py
                python run ChinaFilm/update_releases.py
                python run NRTA/update_records.py
  Alternatively, One can use the corresponding jupyter notebooks to update and review records.


(2) Content Analysis Tools
  - Genre classification from short synopsis
  - Time Period classification from short synopsis
  - NER
    - Character Recognition from synopsis
  - Key phrase/word idenfication using 
    - abstractive title prediction
    - extractive title prediction
    - TF-IDF keyword extraction
  - WIP
    - Story Progression Similarity Comparison

** Screenplay is no longer part of the Content module, it is now a standalone repository. Screenplay is used for auto screenplay formatting, translation and synopsis generation.
** Article is no longer part of the Content module, it is now a standalone repository for generating data overview articles.
