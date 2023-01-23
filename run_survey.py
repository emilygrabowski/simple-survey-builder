# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 12:15:40 2023

@author: Emily Grabowski

Run Survey 

Currently looks for 1: a pkl file 
"""

import config
import pickle
from survey_components import Survey

#while true:

try:
    with open('survey.pkl','rb') as f: 
        survey = pickle.load(f)
        survey.done = False

except:
    print("Can't find an existing survey file. Configuring a survey now:")
    print(config.question_config['question'])
    survey = Survey('inventory.csv',config.question_config)
while not survey.done:
    survey.sample_file()
    
#save progress  
with open('survey.pkl', 'wb') as f:
    pickle.dump(survey,f)
    