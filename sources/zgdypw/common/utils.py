# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 10:09:52 2021

@author: Herais
"""
import os
#import shutil
import pandas as pd
import datetime
#%%
class DB(object):
    
    def __init__(self):
        super(DB, self).__init__()
        
    @staticmethod
    def save_json(df: pd.DataFrame, 
                     filename: str,
                     path_records: str = 'records',
                     backup=True) -> None:
        """
        This functions saves pd.DataFrame to json files with backup option
        """
        dt = datetime.datetime.now()
        appendix_dt = '_{}_{}'.format(str(dt.strftime("%Y%m%d")), 
                                      str(dt.strftime("%H%M"))
                                     )      
        path_file = path_records + '/' + filename + '.json'
        path_file_bk = path_records + '/backup/' + filename + appendix_dt + '.json'
        
        if backup:
            if os.path.isfile(path_file):
                os.rename(path_file, path_file_bk)
        
        df.to_json(path_file)
        print('records saved to: {}, with {} records'.format(path_file, 
                                                          df.shape[0])
             )
        
    @staticmethod
    def save_search(df: pd.DataFrame,
                    path_searches: str = 'searches',
                    suffix:str = ''
                   ) -> None:
        """
        This function saves the current search result in json

        Parameters
        ----------
        df : pd.DataFrame
            DESCRIPTION.
        path_searches : str, optional
            DESCRIPTION. The default is 'searches'.

        Returns
        -------
        None
            DESCRIPTION.

        """
        dt = datetime.datetime.now()
        appendix_dt = '_{}_{}'.format(str(dt.strftime("%Y%m%d")), 
                                      str(dt.strftime("%H%M"))
                                     )     
        path_file = path_searches + '/' + 'search{}_{}.json'.format(
            '_{}'.format(suffix), appendix_dt)
        df.to_json(path_file)
        print('records saved to: {}, with {} records'.format(path_file, 
                                                          df.shape[0])
             )
        
    @staticmethod
    def update_from_search(df_search: pd.DataFrame,
                           fn:str='db',
                           path_records:str='records',
                           path_searches:str = 'searches',
                          ) -> pd.DataFrame:
        """
        This function updates json records by incorporating the latest
        search results.

        Parameters
        ----------
        df_search : pd.DataFrame
            DESCRIPTION.
        fn : str, optional
            DESCRIPTION. The default is 'db'.
        path_records : str, optional
            DESCRIPTION. The default is 'records'.
        path_searches : str, optional
            DESCRIPTION. The default is 'searches'.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        df = pd.DataFrame(columns=['fid'])
        if os.path.isfile(path_records + '//' + fn):
           df = pd.read_json(path_records + '//' + fn)
        
        df_old = df[~df['fid'].isin(df_search['fid'])]
        df_latest = pd.concat([df_search, df_old], ignore_index=True)
        df_latest.reset_index(drop=True, inplace=True)
                
        return df_latest