#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:46:28 2022

@author: Tessa
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import statsmodels.api as sm
from statsmodels.graphics.mosaicplot import mosaic
sns.set_style("whitegrid")

#Here I will attempt a heat map. First I will build a dataset of all the entries for the top 10 states
#using a query and append. 

resto_loans_hm = pd.read_pickle('resto_loans_percap.zip')
state_pop = pd.read_pickle('pop.zip')
state_totals=pd.read_pickle('state_total.zip')



full_WI=resto_loans_hm.query('ProjectState == "WI"') #1
full_OH=resto_loans_hm.query('ProjectState == "OH"') #2
full_MI=resto_loans_hm.query('ProjectState == "MI"') #3
full_NJ=resto_loans_hm.query('ProjectState == "NJ"') #4
full_GA=resto_loans_hm.query('ProjectState == "GA"') #5
full_FL=resto_loans_hm.query('ProjectState == "FL"') #6
full_TX=resto_loans_hm.query('ProjectState == "TX"') #7
full_NY=resto_loans_hm.query('ProjectState == "NY"') #8
full_IL=resto_loans_hm.query('ProjectState == "IL"') #9
full_CA=resto_loans_hm.query('ProjectState == "CA"') #10


full_state_hm=full_WI.append([full_OH, full_MI, full_NJ, full_GA, full_FL, full_TX, full_NY, full_IL, full_CA ], ignore_index=True)


#%%
#This block of code will use a dictionary to replace the NAICS codes with what they actually are,
#stack and unstack a summed state dataset by industry, and use this to make a heatmap.

full_state_hm_1=full_state_hm.replace({"722110": "Full-Service Restaurants",
             "722211": "Limited-Service Rest.",
             "722212": "Cafeterias",
             "722213": "Non-alcoholic Bars",
             "722310": "Food Service Contractors",
             "722320": "Caterers",
             "722330":" Mobile Food Services",
             "722410": "Bars"})


full_state_hm_2=full_state_hm_1.groupby(by=['ProjectState','NAICSCode'])
full_state_sum=full_state_hm_2['CurrentApprovalAmount'].sum()
heatmap=full_state_sum.unstack('ProjectState')
heatmap.fillna(value=0, inplace=True) 


fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("Funding by NAICS Code in Top 10 States")
sns.heatmap(heatmap, ax=ax1)

plt.xlabel("State")
plt.ylabel("Industry by NAICS Code")

fig.tight_layout()

fig.savefig("heatmap.png")



full_state_hm_1=full_state_hm.replace({"722110": "Full-Service Restaurants",
             "722211": "Limited-Service Rest.",
             "722212": "Cafeterias",
             "722213": "Non-alcoholic Bars",
             "722310": "Food Service Contractors",
             "722320": "Caterers",
             "722330":" Mobile Food Services",
             "722410": "Bars"})


full_state_hm_2=full_state_hm_1.groupby(by=['ProjectState','NAICSCode'])
full_state_sum=full_state_hm_2['CurrentApprovalAmount'].sum()
heatmap=full_state_sum.unstack('ProjectState')
heatmap.fillna(value=0, inplace=True) 


fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("Funding by NAICS Code in Top 10 States")
sns.heatmap(heatmap, ax=ax1)

plt.xlabel("State")
plt.ylabel("Industry by NAICS Code")

fig.tight_layout()

fig.savefig("heatmap_state.png")
#%%
#Next I will build a dataset of all the entries for the top 10 cities
#using a query and append. 

full_sd=resto_loans_hm.query('ProjectCity == "SAN DIEGO"') #1
full_dallas=resto_loans_hm.query('ProjectCity == "DALLAS"') #2
full_sf=resto_loans_hm.query('ProjectCity == "SAN FRANCISCO"') #3
full_lv=resto_loans_hm.query('ProjectCity == "LAS VEGAS"') #4
full_mia=resto_loans_hm.query('ProjectCity == "MIAMI"') #5
full_atl=resto_loans_hm.query('ProjectCity == "ATLANTA"') #6
full_hous=resto_loans_hm.query('ProjectCity == "HOUSTON"') #7
full_los=resto_loans_hm.query('ProjectCity == "LOS ANGELES"') #8
full_nyc=resto_loans_hm.query('ProjectCity == "NEW YORK"') #9
full_chi=resto_loans_hm.query('ProjectCity == "CHICAGO"') #10

full_city_hm=full_sd.append([full_dallas, full_sf, full_lv, full_mia, full_atl, full_hous, full_los, full_nyc, full_chi], ignore_index=True)

#The keys for the top ten cities are : SAN DIEGO, DALLAS, SAN FRANCISCO, LAS VEGAS,
#MIAMI, ATLANTA, LOS ANGELES, HOUSTON, NEW YORK, CHICAGO

#%%

#Here I am using the same dictionary to replace and rename the codes.

full_city_hm_1=full_city_hm.replace({"722110": "Full-Service Restaurants",
             "722211": "Limited-Service Rest.",
             "722212": "Cafeterias",
             "722213": "Non-alcoholic Bars",
             "722310": "Food Service Contractors",
             "722320": "Caterers",
             "722330":" Mobile Food Services",
             "722410": "Bars"})
#%%
#Here I am using the same heatmap form to understand how funding varied across NAICS Codes in the top 10 cities.

full_city_hm_2=full_city_hm_1.groupby(by=['ProjectCity','NAICSCode'])
full_city_sum=full_city_hm_2['CurrentApprovalAmount'].sum()
heatmap_city=full_city_sum.unstack('ProjectCity')
heatmap_city.fillna(value=0, inplace=True) 


fig, ax1 = plt.subplots(dpi=300)
fig.suptitle("Funding by NAICS Code in Top 10 Cities")
sns.heatmap(heatmap_city, ax=ax1)
plt.xlabel("Project City")
plt.ylabel("Industry by NAICS Code")
fig.tight_layout()

fig.savefig("heatmap_cities.png")

