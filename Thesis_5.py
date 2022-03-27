#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:45:35 2022

@author: Tessa
"""

#In this script I will analyze loans per capita. I will do this by using an api call to gather state level population data.
#Additional analysis could be done to find the per capita funding on the city level.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
sns.set_style("whitegrid")


resto_loans_percap = pd.read_pickle('resto_loans_readytograph.zip')
state_total_pc = pd.read_pickle('state_total.zip')
#%%

#In this block of code I will use an API to get the population by state. This will be used to find the PPP restaurant loans by state, per capita.

var_list=["NAME","B01001_001E"]

var_string = ",".join(var_list)

api = 'https://api.census.gov/data/2018/acs/acs5'

for_clause = 'state:*'

key_value = "f4de5ccf54be20179eaea5dbf9c2ea66952f031f"

payload= {'get': var_string , 
          'for': for_clause,
          'key': key_value}

response=requests.get(api, payload)
#now moving it to a data frame
row_list = response.json()
colnames = row_list[0]
datarows = row_list[1:]
pop=pd.DataFrame(columns=colnames, data=datarows)

pop.rename(columns={'NAME': 'ProjectState'}, inplace=True)

notcon = ['Alaska','Hawaii','Puerto Rico']

is_conus = pop['ProjectState'].isin(notcon) == False

pop['ProjectState'] = pop[ is_conus ]

print( '\nFiltered length:', len(pop) )

#I ran into key issues so I used this dictionary to do some renaming.
pop_corr=pop.replace({'Alabama':'AL',
             'Arizona': 'AZ',
             'Arkansas': 'AR',
             'California': 'CA',
             'Colorado': 'CO',
             'Connecticut': 'CT',
             'Delaware': 'DE',
             'District of Columbia': 'DC',
             'Georgia': 'GA',
             'Florida': 'FL',
             'Idaho': 'ID',
             'Illinois': 'IL',
             'Indiana': 'IN',
             'Iowa': 'IA',
             'Kansas':'KS',
             'Kentucky': 'KY',
             'Louisiana': 'LA',
             'Maine': 'ME',
             'Maryland': 'MD',
             'Massachusetts': 'MA',
             'Michigan': 'MI',
             'Minnesota': 'MN',
             'Mississippi' :'MS',
             'Missouri': 'MO',
             'Montana': 'MT',
             'Nebraska': 'NE',
             'Nevada' : 'NV',
             'New Hampshire': 'NH',
             'New Jersey' : 'NJ',
             'New Mexico': 'NM',
             "New York": 'NY',
             'North Carolina': 'NC',
             'North Dakota' : 'ND',
             'Ohio': 'OH',
             'Oklahoma': 'OK',
             'Oregon': 'OR',
             'Pennsylvania':'PA',
             'Rhode Island' :'RI',
             'South Carolina' :'SC',
             'South Dakota': 'SD',
             'Tennessee': 'TN',
             'Texas' : 'TX',
             'Utah' : 'UT',
             'Vermont': 'VT',
             'Virginia' : 'VA',
             'Washington': 'WA',
             'West Virginia' : 'WV',
             'Wisconsin': 'WI',
             'Wyoming': 'WY'})

print (len(pop_corr))

pop_corr.to_csv('pop.csv', index=False)


#%%

#Here is the state totals merged with the population we just did.
state_total_pc=state_total_pc.merge(pop_corr,
                              on='ProjectState', 
                              how='left')

#%% Now I will find the PPP loans amounts by state.


state_total_pc['B01001_001E']=state_total_pc['B01001_001E'].astype(float)
state_total_pc['loan_percap']=state_total_pc['CurrentApprovalAmount']/state_total_pc['B01001_001E']
state_total_g=state_total_pc.sort_values('loan_percap').iloc[-20:]

#This is a bar plot to visualize the loans per capita across the top 20 states. DC isn't a state yet (as of May 2021 but maybe soon?) but sure got some funding.

fig, ax1 = plt.subplots()
sns.barplot(x='ProjectState', y='loan_percap', data=state_total_g, ax=ax1)
plt.ylabel('Loans per capita in dollars')
plt.xlabel('States')
plt.title('Top 20 States per Capita for PPP Restaurant Loans')
fig.savefig('loanspercap.png', dpi=300)

#%%

#Now I will do a bit of additonal graphing of the top 10 and bottom 10 states.

states_select=state_total_pc['CurrentApprovalAmount'].sort_values(axis='index')

top_10_states=state_total_pc.sort_values('CurrentApprovalAmount').iloc[-10:]
bottom_10_states=state_total_pc.sort_values('CurrentApprovalAmount').iloc[:10]

#Now I create a graph of top 10 states...


fig, ax1 = plt.subplots()
sns.barplot(x='ProjectState', y='CurrentApprovalAmount', data=top_10_states, ax=ax1)
plt.ylabel('Dollars')
plt.xlabel('State')
plt.title('Top 10 States Recieving Restaurant PPP Loans' )
fig.savefig('top10states_loan.png', dpi=300)

#and a graph of bottom 10 states.

fig, ax1 = plt.subplots()
sns.barplot(x='ProjectState', y='CurrentApprovalAmount', data=bottom_10_states, ax=ax1)
plt.ylabel('Dollars')
plt.xlabel('State')
plt.title('Lowest 10 States Recieving Restaurant PPP Loans' )
fig.savefig('bottom10states_loan.png', dpi=300)


#%%

#This is a graph of the top cities that recieving PPP funding for their restaurants. Note: this focused on project city, not borrower city. 
city_total=resto_loans_percap.groupby("ProjectCity")['CurrentApprovalAmount'].sum()
city_total=city_total.to_frame()

city_total_top10=city_total.sort_values('CurrentApprovalAmount').iloc[-10:]

fig=sns.catplot(y='ProjectCity', x='CurrentApprovalAmount', data=city_total_top10.reset_index(), ax=ax1, kind='bar', orient='h')
plt.ylabel('Cities')
plt.xlabel('Dollars')
fig.tight_layout()
plt.title('Top 10 Cities Recieving PPP Restaurant Loans')
fig.savefig('cityamts.png', dpi=300)

#%%
pop.to_pickle('pop.zip')
state_total_pc.to_pickle('state_totals_pc.zip')
resto_loans_percap.to_pickle('resto_loans_percap.zip')
city_total.to_pickle('city_total.zip')