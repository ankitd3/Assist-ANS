#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
import pandas as pd
from gensim.models import KeyedVectors
import time
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

#x=find_department('Mortage requirements specified are incorrect', False)
def find_department(single_query,only_department):
    #Load model----------------------------------------------------------------------
    st = time.time()
    wordmodelfile = '~/Documents/STUDY/Hackathon/NLP/GoogleNews-vectors-negative300.bin'
    wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True, limit=200000)
    et = time.time()
    s = 'Word embedding loaded in %f secs.' % (et-st)
    print(s)
    #Preprocessing----------------------------------------------------------------------
    single_query_cleaned = clean_set([single_query])[0]
    
    if(len(single_query_cleaned)==0):
        return False
    
    data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/resolved.csv")

    if(only_department == False):
        
        queries = data['query']
        
        _list = queries.values.tolist()
        
        #Cleaned data
        newDataset = clean_set(_list)
        
        x=return_key(3,single_query_cleaned,newDataset,wordmodel)
        if(x!=0):
            x=_list[newDataset.index(x)]
            return fetch_query_details(x,0,'resolved')
    
    #print('here 2')
    #departments = pd.unique(data['Product'])         Sample departments
    keys = ['security', 'loans', 'accounts', 'insurance', 'investments',
       'fundstransfer', 'cards']
    
    #For each element in newDataset (Query) we find the most similar key (Department) mode=0
    department=return_key(5,single_query_cleaned,keys,wordmodel)
    #Returning depart
    q_id = log_query(max(data['query_id'])+1,single_query,department)
    
    return department,q_id

def change_department(q_id, new_department):
    data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv")
    i=data[data['query_id']==q_id].index.values[0]
    #print(i)
    data.set_value(i,"department", new_department)    
    data.to_csv('~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv', encoding='utf-8', index=False)

def clean_set(_list):
    newDataset=[]
        
    for response in _list:
        #Lower, remove punctuations and strip white-spaces and split by spaces
        response_words=response.lower().translate(str.maketrans('', '', string.punctuation)).strip().split()
        response=''
        for word in response_words:
            if word not in ENGLISH_STOP_WORDS:
                response+=word+' ' 
        newDataset.append(response[:-1])
    
    return newDataset
#resolve_query(62,521,'What to do eh?')

def resolve_query(query_id,employee_id,solution):
    from datetime import date
    today = date.today().strftime("%d/%m/%Y")
    
    d = fetch_query_details('',query_id,'unresolved')
    
    query_date = d[0][3]
    d[0][3] = solution
    d[0] = d[0] + [query_date,today,employee_id]
    
    unresolved_data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv")

    unresolved_data = unresolved_data[unresolved_data.query_id != query_id]
    unresolved_data.to_csv('~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv', encoding='utf-8', index=False)
    
    new_data = pd.DataFrame(d, columns = ['query_id','query','department','solution','query_date','date_solved','employee_id'])
    data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/resolved.csv")
    data = pd.concat([data, new_data])
    
    data.to_csv('~/Documents/STUDY/Hackathon/NLP/dataset/resolved.csv', encoding='utf-8', index=False)
    #new_data = pd.DataFrame([d], columns = ['query_id','query','department','query_date'])
    

def log_query(query_id, query, department):
    from datetime import date
    today = date.today().strftime("%d/%m/%Y")
    d=[query_id,query,department,today]
    
    new_data = pd.DataFrame([d], columns = ['query_id','query','department','query_date'])
    
    try:
        data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv")
        if(len(data)>0):
            test = True
        else:
            test = False
    except:
        test = False
    
    if(test):
        new_data.at[0, 'query_id'] = max(max(data['query_id'])+1,query_id)
        data = pd.concat([data, new_data])
    else:
        data = new_data    
    
    data.to_csv('~/Documents/STUDY/Hackathon/NLP/dataset/unresolved.csv', encoding='utf-8', index=False)
    
    return data.loc[data['query'] == query].values.tolist()[0]

#----------------------------------------------------------------------
def fetch_query_details(text,query_id,file_name):
    data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/dataset/"+file_name+".csv")
    if(text == 'all'):
        return data.values.tolist()
    elif(query_id==0):
        return data.loc[data['query'] == text].values.tolist()
    else:
        return data.loc[data['query_id'] == query_id].values.tolist()

def return_key(threshold,sentence_a,keys,wordmodel):
    sentence_a = sentence_a.lower().split()
    distance_list = []
    for key in keys:
        sentence_b = key.lower().split()
        distance_list.append(wordmodel.wmdistance(sentence_a, sentence_b))
    #print(min(distance_list))
    if(min(distance_list)>threshold):
        return 0
    return(keys[distance_list.index(min(distance_list))])
'''
data = pd.read_csv("~/Documents/STUDY/Hackathon/NLP/Consumer_Complaints.csv",nrows=500)
    #218 queries

xtrain = data.loc[data['Consumer complaint narrative'].notnull(), ['Consumer complaint narrative','Product','Company public response']]

xtrain = xtrain.loc[xtrain['Company public response'].notnull(), ['Consumer complaint narrative','Product','Company public response']]

xtrain.to_csv('./dataset/resolved.csv', encoding='utf-8', index=False)
'''
#print(find_department('credit repair services'))
#SAVING----------------------------------------------------------------------    
