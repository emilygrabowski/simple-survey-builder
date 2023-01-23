# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 15:20:11 2023

@author: Emily Grabowski


Classes to help build the survey, including properties and functions

"""
import pandas as pd
import os


class SurveyQuestion:
    '''Class for each question of the survey'''
    def __init__(self,question,resp_book,label,level):
        self.question = question
        self.label = label
        self.valid = False
        self.input = None
        self.output = None
        self.resp_map = resp_book
        self.level = level
        self.validate_map()
    
    def validate_map(self):
        '''check the response map for certain issues. Issues checked so far:
         - duplicate values in multiple keys
         Automatically done when the map is input
        '''
        all_values = [i for sl in list(self.resp_map.values()) if not sl == None for i in sl if not sl == None] #make a list of inputs
        dups = pd.Series(all_values,index=all_values).duplicated(keep=False)
        if sum(dups>0):
            print("The following values appear to be duplicated:",set(dups.loc[dups].index))
        
    def get_input(self):
        self.input = input(self.question).lower().strip()
    
    def validate(self):
        '''validate the input by checking that it corresponds to a part of the map'''

        if None in pd.Series(self.resp_map.values()).explode().values:
            print("There is a catch option. All entries are valid.")
            self.valid=True
        elif self.input in pd.Series(self.resp_map.values()).explode().values:
            #print("Item validated")
            self.valid=True            
        else:
            print("Validation failed. Please try again")
    
 
    def evaluate(self):
        '''translate from input to standardized forms using the response map'''
        for k,v in self.resp_map.items():
            if type(v) == str:
                v = [v]
            if v == None:
                catch = k
            elif self.input in v:
                self.output= k
        if self.output == None:
            self.output = catch
        
            
        
    def ask(self):
        '''Function connecting the workflow'''
        while not self.valid:
            self.get_input()
            self.validate()
        self.evaluate()
    
class Sample:
    '''Class used to control question flow'''
    def __init__(self,questions,item):
        self.qs = []
        self.qlevels = questions['level']
        self.metadata = item
        self.done= False
        self.summary = dict()
        self.summary_paper = pd.DataFrame()
        
        #generate question objects for each question
        for ix,q in questions.iterrows():
            self.qs.append(SurveyQuestion(q['question'],q['validation'],
                                          q['label'],q['level']))
    
    
    def update_summary(self,q,level):
        self.summary[q.label] = [q.output]
            
    def print_summary(self):
        '''basic summmary'''
        print(pd.DataFrame(self.summary))
        

    def analyze_sample(self):
        '''Overall flow of the survey.
        Can run in an IDE console or in the command line'''
        
        #open PDF
        os.startfile(self.metadata['file'].values[0])
        qlist = self.qs
        while not self.done:
            for q in qlist:
                q.ask()
                self.update_summary(q,q.level)
            print("all questions answered. Here is a summary:")
            self.print_summary()
            
            #option to fix answers
            review = input("Press enter to accept or type the name of the question that you want to review").split(',')
            qlist = []
            if review == ['']:
                self.summary_paper = pd.concat([self.summary_paper,pd.DataFrame(self.summary)])
                
                #option to add in a partially overlapping entry for the same paper
                return_or_finish =  input("Press enter to finish for this paper, e to exit, or the number of level you wish to add:")
                if return_or_finish =='e': #save result and exit
                    self.done = True
                    for m in list(self.metadata):
                        self.summary_paper[m]=self.metadata[m].values
                    self.summary_paper['analyzed'] = True
                    print(self.summary_paper)
                    return(self.summary_paper,True)
                elif return_or_finish == '': #save result and go to next paper
                    self.done = True
                    for m in list(self.metadata):
                        self.summary_paper[m]=self.metadata[m].values
                    print(self.summary_paper)

                    self.summary_paper['analyzed'] = True
                    return(self.summary_paper,False)
                else: #add another entry for this paper
                    qlist = [q for q,l in zip(self.qs,self.qlevels) if l >= int(return_or_finish)]
                    for q in qlist:
                        q.valid = False
            else:  #review some entries for this result
                for r in review:
                    for q in self.qs:
                        if q.label == r.strip().lower():
                            q.valid = False
                            qlist.append(q)
                print('to review',qlist)

        
class Survey:
    '''class for assembling, querying, and maintaining the entire survey'''
    def __init__(self,data_file,question_config):
        self.inventory= pd.read_csv(data_file)
        self.inventory['analyzed'] = False
        self.survey = pd.DataFrame(columns = list(question_config['label']) +
                                   (list(self.inventory)))
        self.survey_questions = question_config
        self.done= False

        
    def sample_file(self):
        if not len(self.inventory.loc[~self.inventory['analyzed'],:])==0:
            item = self.inventory.loc[~self.inventory['analyzed'],:].sample(1)
            s,self.done = Sample(self.survey_questions,item).analyze_sample()
            self.survey = pd.concat([self.survey,s])
            self.inventory.loc[item.index,'analyzed']=True
        else:
            print("All files analyzed")
            self.done=True
        
    def summary(self):
        print("So far you have analyzed", self.survey['file'].nunique(),'files')

