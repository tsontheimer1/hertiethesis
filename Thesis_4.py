#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:44:55 2022

@author: Tessa
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
sns.set_style("whitegrid")

#In this script I will create some graphs and plots about the PPP data for restaurants. 

#%%
#Here I am importing and doing a log on current approval amounts for the PPP loans for restaurants.
        
resto_loans = pd.read_pickle('resto_loans_readytograph.zip')
state_totals = pd.read_pickle('state_total.zip')


print(resto_loans['CurrentApprovalAmount'].describe())
resto_loans['log_currentapprovalamount']=np.log(resto_loans['CurrentApprovalAmount'])
print(resto_loans['log_currentapprovalamount'].describe())
print(resto_loans['JobsReported'].describe())

#%%

#Now we will create other data frames that cut the lowest 99% of Jobs Reported and the outliers about 99% for the Current Loan Approval. 

resto_loans['JobsReported']=pd.to_numeric(resto_loans['JobsReported'], downcast='float')

caa99 = resto_loans["CurrentApprovalAmount"].quantile(0.99)

jrt99 = resto_loans["JobsReported"].quantile(0.99)

#Here we are doing it at the 90th percentile to illustrate it a bit more.

jrt50 = resto_loans["JobsReported"].quantile(0.5)

jrt75 = resto_loans["JobsReported"].quantile(0.75)

print("Here is the current approval amount at the 99th percentile:")
print (caa99)

print("Here is the jobs reported at the 99th and 75th percentile, respectively. They will be trimmed below in two variables called jrt50 and jrt99:")
print(jrt99)
print(jrt75)
#trimm_99 removes the top 1% of the loans through the Current Approval Amount.

#trim_99_2 removes the top 1% of the loans and the bottom 99% of jobs reported. 
trim_99 = resto_loans.query(f"CurrentApprovalAmount <= {caa99} " )
trim_99_2 = resto_loans.query(f"CurrentApprovalAmount <= {caa99} and JobsReported > {jrt99}" )
print(len(trim_99))

trim_75 = resto_loans.query(f"JobsReported >= {jrt75}" )

#%%
#This graph demonstrates the current approval amount of PPP loans for a restaurants 
fig, ax1 = plt.subplots()
trim_99['CurrentApprovalAmount'].plot.hist(ax=ax1)

ax1.set_ylabel('Frequency of Loan Amount')
ax1.set_xlabel('Dollars')
plt.title('Current PPP Approval Amount for Restaurants (99th percentile of loans removed)' )
fig.savefig('CurrentApprovalAmount_trimmmed.png')

#%%
#Now we will create a hex diagram that cuts the lowest 99% of Jobs Reported and the outliers about 99% for the Current Loan Approval. 

fig = sns.jointplot(data=trim_99_2,
              y='CurrentApprovalAmount',
              x='JobsReported',
              kind='hex')
plt.ylabel('Loan in Dollars (99th percentile of loans removed)')
plt.xlabel('Total Jobs Reported (99th percentile of jobs reported shown)')
fig.savefig('resto_hex.png')
#note this doesn't have a title because it doesn't appear properly.

#%%
#To set the title of axes object A to "words" use A.set_title("words"). To set the X label to "words" use A.set_xlabel("words"). 
#Set the Y label in an analogous way.

bins_list=[100, 200, 300, 400, 500]
fig, ax1 = plt.subplots()
resto_loans['JobsReported'].plot.hist(ax=ax1, bins=bins_list)
plt.ylabel('Frequency of Number of Employees')
plt.xlabel('Jobs Reported ')
plt.title('Jobs Reported by Restaurant PPP Loan Recipient with over 100 Jobs Reported')
fig.savefig('jr_over100.png', dpi=300)

bins_list_mini=[0, 2, 4, 6, 8, 10]
fig, ax1 = plt.subplots()
resto_loans['JobsReported'].plot.hist(ax=ax1, bins=bins_list_mini)
plt.ylabel('Frequency of Number of Employees')
plt.xlabel('Jobs Reported')
plt.title('Jobs Reported by Restaurant PPP Loan Recipient with Under 10 Jobs Reported')
fig.savefig('jr_under10.png', dpi=300)

bins_list_med=[0, 20, 40, 60, 80, 100]
fig, ax1 = plt.subplots()
resto_loans['JobsReported'].plot.hist(ax=ax1, bins=bins_list_med)
plt.ylabel('Frequency of Number of Employees')
plt.xlabel('Jobs Reported')
plt.title('Jobs Reported by Restaurant PPP Loan Recipient with Under 100 Jobs Reported')
fig.savefig('jr_under100.png', dpi=300)

#%%
#Now I will make a boxplot of money recieved by NAICS code

fig, ax = plt.subplots( dpi=300)

#I am using this dictionary to do some renaming. 
trim_99_n=trim_99.replace({"722110": "Full-Service Restaurants",
             "722211": "Limited-Service Rest.",
             "722212": "Cafeterias",
             "722213": "Non-alcoholic Bars",
             "722310": "Food Service Contractors",
             "722320": "Caterers",
             "722330":" Mobile Food Services",
             "722410": "Bars"})

sns.boxenplot(x='CurrentApprovalAmount', y='NAICSCode', data=trim_99_n, ax=ax,showfliers=False)
plt.xticks(rotation=45)

ax.legend(loc='upper left',  bbox_to_anchor=(0, 1.1))
fig.savefig('Money_by_NAICS.png', dpi=300)
plt.ylabel('Type of Restaurant by NAICS Code')
plt.xlabel('Dollars' )
plt.title('Current Loan Amount Recieved by Establishment Type (99th percentile and outliers removed)')
fig.savefig('loan_by_est.png', dpi=300)



#%%

#Here is printing some data which is helpful for thinking about how we will understand and visualize our results.

print("Here are some statistics about the data:")
print("\nData about PPP loan amount for a restaurants:")
print(resto_loans['CurrentApprovalAmount'].describe)
print(resto_loans['CurrentApprovalAmount'].mean()) 
print("\nJobs reported for a restaurant recieving a PPP loan:")
print(resto_loans['JobsReported'].describe) 

#%%

top_10k=resto_loans.sort_values('CurrentApprovalAmount').iloc[-10000:]
bottom_10k=resto_loans.sort_values('CurrentApprovalAmount').iloc[:10000]

#%%
 
#This is a graph across loan size and across gender of the loan recipients.
   
fig, ax1 = plt.subplots(dpi=300)
sns.boxenplot(data= trim_99, y="CurrentApprovalAmount", x= "Gender", orient="v", ax=ax1)
ax1.set_title("Current Approval Amount for PPP Restaurant Loans by Gender of Loan Receipent")
ax1.set_xlabel("Gender of Loan Receipent")
ax1.set_ylabel("Restaurant PPP Loan Amount in Dollars (99th percentile removed)")
fig.tight_layout()
fig.savefig("Resto_loans_gender.png", dpi=300)

#%%
#This is a graph across race of the loan recipients.
   
trim_99_n=trim_99.replace({"Black or African American": "Black",
             "American Indian or Alaska Native": "American Indian",
             "Native Hawaiian or Other Pacific Islander": "Native Hawaiian or PI"})

fig, ax1 = plt.subplots(dpi=300)
sns.barplot(data= trim_99_n, y="CurrentApprovalAmount", x= "Race", orient="v", ax=ax1)
ax1.set_title("Current Approval Amount for PPP Restaurant Loans by Race of Loan Receipent")
ax1.set_xlabel("Race of Loan Receipent")
ax1.set_ylabel("Restaurant PPP Loan Amount in Dollars (99th percentile removed)")
plt.xticks(rotation=25)
fig.tight_layout()
fig.savefig("Resto_loans_race.png", dpi=300)