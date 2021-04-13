#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 22:44:40 2020

@author: nehaprakash
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 20:44:13 2020

@author: singh
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from nltk.corpus import stopwords
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import re
import csv

Texts=[]
Job_titles=[]
#with open('/Users/nehaprakash/Documents/CSV_Combined_Final/Combined_Final_CSV.csv', 'r') as csvfile:
with open(r'C:/Users/zubin/Desktop/STEVENS/SEM 3/WEB MINING/Data_Scientists_Menlo_Park/Data_Scientists_Menlo_Park.csv', encoding="utf8") as csvfile:
    reader=csv.reader(csvfile)
    for line in reader:
        Texts.append(line[0])
        Job_titles.append(line[1])    
    print(len(Texts))
    print(len(Job_titles))
    
Texts_train,Texts_test,Job_titles_train,Job_titles_test=train_test_split(Texts,Job_titles,test_size=0.2,random_state=0)

print(len(Texts_train))
print(len(Job_titles_train))
print(len(Texts_test))
print(len(Job_titles_test))

counter = CountVectorizer(stop_words=stopwords.words('english'))
counter.fit(Texts_train)

#count the number of times each term appears in a document and transform each doc into a count vector
counts_train = counter.transform(Texts_train)#transform the training data
counts_test = counter.transform(Texts_test)#transform the testing data

KNN_classifier=KNeighborsClassifier()
LREG_classifier=LogisticRegression(solver='liblinear')
DT_classifier = DecisionTreeClassifier()

predictors=[('knn',KNN_classifier),('lreg',LREG_classifier),('dt',DT_classifier)]
VT=VotingClassifier(predictors)

#build the parameter grid
#KNN_grid = [{'n_neighbors': [5,10], 'weights':['uniform','distance']}]
KNN_grid = [{'n_neighbors': [121,143,175,199,211,233,255,277], 'weights':['uniform','distance']}]

#[1,3,5,7,9,11,13,15,17]
#build a grid search to find the best parameters
#gridsearchKNN = GridSearchCV(KNN_classifier, KNN_grid, cv=2)
gridsearchKNN = GridSearchCV(KNN_classifier, KNN_grid, cv=15)

#run the grid search
gridsearchKNN.fit(counts_train,Job_titles_train)


#build the parameter grid
#DT_grid = [{'max_depth': [None],'criterion':['gini','entropy']}]
DT_grid = [{'max_depth': [1500,1800,2250,2700,3150,3600,4500,4950,5400],'criterion':['gini','entropy']}]

#build a grid search to find the best parameters
gridsearchDT  = GridSearchCV(DT_classifier, DT_grid, cv=15)
#gridsearchDT  = GridSearchCV(DT_classifier, DT_grid, cv=2)

#run the grid search
gridsearchDT.fit(counts_train,Job_titles_train)


#build the parameter grid
LREG_grid = [ {'C':[0.5,1,1.5,2],'penalty':['l1','l2']}]

#build a grid search to find the best parameters
gridsearchLREG  = GridSearchCV(LREG_classifier, LREG_grid, cv=15)
#gridsearchLREG  = GridSearchCV(LREG_classifier, LREG_grid, cv=2)

#run the grid search
gridsearchLREG.fit(counts_train,Job_titles_train)

VT.fit(counts_train,Job_titles_train)

#use the VT classifier to predict
#predicted=VT.predict(counts_test)
predicted=VT.predict(counts_test).tolist()

#Final_Output_File
concat= list(zip(Texts_test,predicted))
df = pd.DataFrame(concat,columns=['Description','Job title'])
df.to_csv(r'final_desc_title.csv',index=False)

#print the accuracy
print (accuracy_score(predicted,Job_titles_test))