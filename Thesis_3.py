#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:43:18 2022

@author: Tessa
"""

import pandas as pd
import numpy as np

#In this script, I will parse out the date of loan approval and create some graphics that explore the 
#nuances of who recieved loans, of what size, and when across restaurants requesting PPP loans.

resto_loans = pd.read_pickle('resto_loans_polished.zip')

#%%
#Here I will do a bit of cleaning. first I will drop any lines that have empty slots for this essential data.

essentials=['BorrowerCity', 'BorrowerState', 'ProjectCity', 'ProjectState', 'Race', 'Ethnicity', 'Gender', 'Veteran', 'DateApproved', 'CurrentApprovalAmount', 'InitialApprovalAmount', 'JobsReported']
resto_loans= resto_loans.dropna(subset=essentials)

#Now I will drop all places that are not in the continential US.
abbrev_notcon = ['AK','AS','GU','HI','MP','PR','VI']

abbrev_conus = resto_loans['ProjectState'].isin(abbrev_notcon) == False

resto_loans_cleaned = resto_loans [ abbrev_conus ]

print( '\nFiltered length:', len(resto_loans_cleaned) )

#%%
#Here I am attempting to find the difference between inital approval amounts and current approval amounts. I used this to use pd.to_numeric (https://www.kite.com/python/answers/how-to-convert-a-pandas-dataframe-column-of-strings-to-floats-in-python#:~:text=Use%20pandas.,the%20column%20values%20to%20floats.)
resto_loans_cleaned = resto_loans_cleaned.copy()
resto_loans_cleaned['CurrentApprovalAmount']=resto_loans_cleaned['CurrentApprovalAmount'].astype(float)
resto_loans_cleaned['InitialApprovalAmount']=resto_loans_cleaned['InitialApprovalAmount'].astype(float)
resto_loans_cleaned['zip']=resto_loans_cleaned['zip'].astype(float)
resto_loans_cleaned['JobsReported']=resto_loans_cleaned['JobsReported'].astype(float)
resto_loans_cleaned['ProjectCity']=resto_loans_cleaned['ProjectCity'].str.upper()


int_loan_amts=resto_loans_cleaned['InitialApprovalAmount']

cur_loan_amts=resto_loans_cleaned['CurrentApprovalAmount']

diff_loan_amts=int_loan_amts-cur_loan_amts
#%%
#Now I will make the DateApproved variable usable for analysis.

date=pd.to_datetime(resto_loans_cleaned['DateApproved'])

resto_loans_cleaned['month']=date.dt.month
resto_loans_cleaned['day']=date.dt.day
resto_loans_cleaned['year']=date.dt.year

#%%
#Here I am creating a few variables that will be useful for analysis and visualization.

resto_loans_cleaned['difference in loan amounts']=diff_loan_amts

jobs_reported=resto_loans_cleaned['JobsReported']

zipcode=resto_loans_cleaned['zip']

rec_gender=resto_loans_cleaned['Gender']

print("Here is some information about the resto_loans_cleaned data frame:")
print(resto_loans_cleaned.info)

#%%
#I will aggregate the data for each state and determine how much PPP funding each state received. I will attempt to make totals for each state. The result will be a dictionary of totals by state.

state_total=resto_loans_cleaned.groupby("ProjectState")['CurrentApprovalAmount'].sum()
print (state_total)

state_total=state_total.to_frame()

print('Here is the total PPP funding for restaurants by state:')

print(state_total.sort_values(by='CurrentApprovalAmount'))
print(len(state_total))



#%%

#This loop will provide a brief peek into some of the characteristics of the categorical data.
catvars=['BorrowerCity', 'BorrowerState', 'ProjectCity', 'ProjectState', 'Race', 'Ethnicity', 'Gender', 'Veteran', 'month']

#for var in catvars:
    #print (var)
    #print (resto_loans_cleaned[var].value_counts())
    #fig=sns.catplot(y=var, data=resto_loans_cleaned, kind='count')

#%%
resto_loans_cleaned.to_csv('resto_loans_readytograph.csv')
resto_loans_cleaned.to_pickle('resto_loans_readytograph.zip')
#resto_loans_cleaned.to_pickle('state_totals_readytograph.zip')
state_total.to_pickle('state_total.zip')
