#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:30:43 2022

@author: Tessa
"""

#In this script I will take the Payroll Protection Program (PPP) 
#loans Freedom of Information Act (FOIA) files into one dataframe for 
#further use in the analysis.

import pandas as pd

#Create a data frame with each CSV file. This data is from May 2, 2021, 9:30 PM (UTC-04:00)
#It can be downloaded at https://data.sba.gov/dataset/ppp-foia 
#All 12 avaiable CSV files will be used

#Here I am loading each csv to a dataframe.

loan1=pd.read_csv('public_up_to_150k_1_220102.csv', dtype=str)

loan2=pd.read_csv('public_up_to_150k_2_220102.csv', dtype=str)

loan3=pd.read_csv('public_up_to_150k_3_220102.csv', dtype=str)

loan4=pd.read_csv('public_up_to_150k_4_220102.csv', dtype=str)

loan5=pd.read_csv('public_up_to_150k_5_220102.csv', dtype=str)

loan6=pd.read_csv('public_up_to_150k_6_220102.csv', dtype=str)

loan7=pd.read_csv('public_up_to_150k_7_220102.csv', dtype=str)

loan8=pd.read_csv('public_up_to_150k_8_220102.csv', dtype=str)

loan9=pd.read_csv('public_up_to_150k_9_220102.csv', dtype=str)

loan10=pd.read_csv('public_up_to_150k_10_220102.csv', dtype=str)

loan11=pd.read_csv('public_up_to_150k_11_220102.csv', dtype=str)

loan12=pd.read_csv('public_up_to_150k_12_220102.csv', dtype=str)

loan13=pd.read_csv('public_150k_plus_220102.csv', dtype=str)

#Now I will compile into one dataframe,

allloans=loan1.append([loan2, loan3, loan4, loan4, loan5, loan6, loan7, loan8, loan9, loan10, loan11, loan12, loan13])

#Now from all the all the loans I will find the businesses that correspond to restaurant or reaturant adjacent businesses
#NAICS codes are sourced from here https://www.census.gov/eos/www/naics/reference_files_tools/1997/sec72.htm#:~:text=722110%20Full%2DService%20Restaurants,service)%20and%20pay%20after%20eating.

resto_naics_dict={"722110": "Full-Service Restaurants",
             "722211": "Limited-Service Resturants",
             "722212": "Cafeterias",
             "722213": "Snack and Nonalcoholic Beverage Bars",
             "722310": "Food Service Contractors",
             "722320": "Caterers",
             "722330":" Mobile Food Services",
             "722410": "Drinking Places (Alcoholic Beverages)"}

resto_naics_list=["722110", "722211", "722212","722213","722310","722320", "722330", "722410"]

is_res = allloans['NAICSCode'].isin(["722110", "722211", "722212", "722213", "722310", "722320", "722330", "722410"])   

resto_loans = allloans[is_res]    

#It is really key to pickle these files so we do not have to re-run all of the CSVs to dataframes each time.
resto_loans.to_pickle('resto_loans.zip')
resto_loans.to_csv('resto_loans_int.csv')

index=resto_loans.index
number_rows=len(index)
print("After combining all the FOIA PPP data and sorting it based upon NAICS codes, the number of PPP loans for restaurants is:")
print(number_rows)

#Here I am just trying to take a peek at some of the features of our data.
print(resto_loans['JobsReported'].describe())