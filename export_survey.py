# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:54:26 2023

@author: Emily Grabowski

Simple script to export the results of the survey
"""

import pandas as pd
import pickle
try:
    with open('survey.pkl','rb') as f: 
        survey = pickle.load(f)
        survey.survey.to_csv('output.csv',index=False)
except:
    print('No survey found.')