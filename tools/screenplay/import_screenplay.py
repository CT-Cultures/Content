# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 01:14:16 2020

@author: VSurfacePro3
"""

#%% Import Libraray
import pandas as pd
import numpy as np

import os
#%% Define Class

class ScreenPlay(object):
    
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        super(ScreenPlay, self).__init__()        

#%% Class Import

class comform_Screenplay(object):
    
    def __init__(self, filepath: str):
        
        super(comform_Screenplay, self).__init__()
        
        self.filepath = filepath
        
    
    def source_type(self, filepath: str):
        extension = filepath[-5:-1].split('.')
        if len(extension) > 1:
            return extension[1]
        else:
            return 'Unknown'
        
    def openfile(self, 
                 filepath: str, 
                 encoding: str = 'utf-8-sig',
                 force_open: bool = False
                 ) -> pd.DataFrame:

        data = pd.DataFrame()
        source_type = self.source_type(filepath)
        if source_type == 'Unknown':
            print 'Unknown Filetype'
        
        elif filetype == 'txt':
            data = pd.read_text(filepath, eoncoding=encoding)
            
        elif filetype == 'csv':
            data = pd.read_csv(file_ath, encoding=encoding)
            
        return data
            
            