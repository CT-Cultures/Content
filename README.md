# Content

This Project creates a set of tools for collecting and updating Entertainment Content Data, and periodically generate articles for downstream publications on social networks. These tools are designed for collaborating colleagues with minimal programming knowledge.

(1) Currently supported Data Sources
  - ChinaFilm, including film registration and release permit records.
  - NRTA, including TV registration records, will gradually include
  
  Sample Usage: python rum ChinaFilm/update_registrations.py
                python run ChinaFilm/update_releases.py
                python run NRTA/update_records.py
  Alternatively, One can use the corresponding jupyter notebooks to update and review records.

(2) Article Generation Tools
  - Film Registrations Overview, 
  -Generate a docx for each film release publication, with highlights on project age, title changes and registered organization change.


(3) Content Analysis Tools
  - Genre classification from short synopsis
  - Time Period classification from short synopsis
  - NER
    - Character Recognition from synopsis
  - Key phrase/word idenfication using 
    - abstractive title prediction
    - extractive title prediction
    - TF-IDF keyword extraction
  - WIP
    - Story Semantic Similarity Comparision

** Screenplay is no longer part of Content module, it is now a standalone repository. Screenplay is used for auto screenplay formatting, translation and synopsis generation.
