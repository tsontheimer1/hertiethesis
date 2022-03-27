#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:42:45 2022

@author: Tessa
"""

#In this script I will remove all zips that are not 5 or 9, trim them, remove unnecessary columns, and create a new polished pickle.

import pandas as pd

resto_loans = pd.read_pickle('resto_loans.zip')

print(resto_loans['JobsReported'].describe())

print(resto_loans['JobsReported'].max())

#%%

zip_all = resto_loans['ProjectZip']

ziplen=zip_all.str.len()

print("\nHere are zipcode lengths:")
print (ziplen.value_counts(dropna=False))

#In this portion of the script I am cleaning and organizing the zip codes. 

zip_9 = ziplen == 10

#Note that this is 10 not 9 because of the "-" that is included. In a string this is "10" but is a 9-digit zip.

zip_5 = ziplen == 5

zip_ok = zip_5 | zip_9

zip_bad = ~ zip_ok

zip5=zip_all.copy() 

zip5[zip_9] = zip5[zip_9].str[:5]

zip5[zip_bad]=None

zip5len = len(zip5)

print("\nHere's the corrected 5 digit zips and the value counts across the zips. The highest 30349 is in Atlanta, GA.")
print(len(zip5))
print ("\n")
print (zip5.value_counts(dropna=False))

resto_loans['zip']=zip5

#Here I am dropping some unnecessary columns.

resto_loans_polished=resto_loans.drop(['SBAOfficeCode', 'ProcessingMethod', 'LoanStatusDate', 'SBAGuarantyPercentage', 'FranchiseName',	
 'ServicingLenderLocationID', 'ServicingLenderName', 'ServicingLenderAddress',	'ServicingLenderCity', 'ServicingLenderState',
 'ServicingLenderZip', 'UTILITIES_PROCEED',	'PAYROLL_PROCEED', 'MORTGAGE_INTEREST_PROCEED',	 'RENT_PROCEED',
'REFINANCE_EIDL_PROCEED','HEALTH_CARE_PROCEED',	'DEBT_INTEREST_PROCEED',
'OriginatingLenderLocationID', 'OriginatingLender', 'OriginatingLenderCity', 'OriginatingLenderState','NonProfit'], 
                             axis='columns')

resto_loans_polished.to_pickle('resto_loans_polished.zip')