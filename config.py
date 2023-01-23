# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 12:25:49 2023

@author: Emily Grabowski
"""

import pandas as pd

true_std_bin = {'T':['y'],'F':['','n']}
#false_std_bin = {'T':['y',''],'F':['n']}

text_val_1 = {'consonant':['c','cons','consonant'],
           'vowel':['v','vowel']}

question_config = pd.DataFrame({'label':['include','category'],
                                'question':['Is this an acoustics paper? y/n',
                                                'Is this a vowel or consonant paper?'],
                                'validation':[true_std_bin,text_val_1],
                                'level':[0,1]})

