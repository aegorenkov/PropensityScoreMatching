---------------------------
Author:Alexander Egorenkov
Date: May 15th, 2015
----------------------------
This directory contains test data files for a propensity score matching routine
in python. The intention is to use psmatch2 results to gauge the accuracy of 
the new routine.
-------------------------------
Original data files can be found at "users.nber.org/~rdehejia/nswdata2.html"

"Causal Effects in Non-Experimental Studies: Reevaluating the Evaluation of 
Training Programs," Journal of the American Statistical Association, Vol. 94, 
No. 448 (December 1999), pp. 1053-1062. 
--------------------------
File descriptions:

Original data: [nswre74_control.txt, nswre74_treated.txt]
-The variables are as follows, explanations can be found at the posted url.
Treated: treatment indicator (1 if treated, 0 if not treated) 
Age: age
Eduction: education
Black: Black (1 if black, 0 otherwise)
Hispanic: Hispanic (1 if Hispanic, 0 otherwise)
Married: married (1 if married, 0 otherwise)
Nodegree: nodegree (1 if no degree, 0 otherwise)
RE74: RE74 (earnings in 1974)
RE75: RE75 (earnings in 1975)
RE78: RE78 (earnings in 1978)

Scripts: [prepare_psm_testdata.do]
-This file contains the routine to generate the test data in STATA 13
-We generate 12 csv files. 4 csv files with randomly sorted versions of the 
Dehejia and Wahha data, 4 csv files that run a simple PSM on each randomly 
sorted file and 4 csv files that run a more extensive PSM.

DTA files: [nsw_control.data, nsw_treated.dta, nsw_all.dta]
-These are intermediate STATA files to join the treatment and control data

