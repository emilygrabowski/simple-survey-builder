# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 16:22:45 2023

@author: Emily Grabowski

Script to create the inventory file. This file will contain the metadata

The metadata file should have a column 'file' and can have other columns
containing metadata
"""
import pandas as pd
import os
import glob
def get_metadata(data_dir,update=True):
    '''supports either a file that has a column with text in it
    or a file that has a column with filenames in it'''
    if (os.path.exists(data_dir)) and not update:
        inventory = pd.read_csv(data_dir)
    else:
        print('generating inventory from directory')
        inventory = pd.DataFrame({'file':[x for x in glob.glob(data_dir,recursive=True)]})
        #example metadata
        inventory['journal'] = "Journal of Phonetics"
    return(inventory)
inventory = get_metadata('sample-data/*pdf')
inventory.to_csv('inventory.csv',index=False)

