***************************************************************
*** Author: Alexander Egorenkov  (Resources for the Future) ***
*** Prepared for: Allen Blackman (Resources for the Future) ***
***************************************************************
*Originally run on STATA 13
*NOTE: psmatch2 required

*set working directory here for portability
cd M:\Blackman\PropensityScoreMatching\PropensityScoreMatching\tests\results\generate_test_files

*Import Lalonde data as used by Dehejia and Wahha (treatment group)
import nswre74_treated.txt, delimiter(whitespace, collapse) varnames(nonames) clear 
*Give names to variables
drop v1
rename v2 Treated
rename v3 Age
rename v4 Education
rename v5 Black
rename v6 Hispanic
rename v7 Married
rename v8 Nodegree
rename v9 RE74
rename v10 RE75
rename v11 RE78

*Save as DTA for later use in STATA
saveold "nsw_treated.dta", replace

*Import Lalonde data as used by Dehejia and Wahha (control group)
import delimited nswre74_control.txt, delimiter(whitespace, collapse) varnames(nonames) clear 
*Give names to variables
drop v1
rename v2 Treated
rename v3 Age
rename v4 Education
rename v5 Black
rename v6 Hispanic
rename v7 Married
rename v8 Nodegree
rename v9 RE74
rename v10 RE75
rename v11 RE78

*Save as DTA for later use in STATA
saveold "nsw_control.dta", replace

*Join treatment and control sets together
append using "nsw_treated.dta"

*Save as DTA for later STATA use
saveold "nsw_all.dta", replace

***********************************************************************
*Create randomly sorted datasets for testing propensity score matching*
***********************************************************************

use "nsw_all.dta", clear
set seed 12345
gen sortorder = runiform()
sort sortorder
drop sortorder
export delimited using "nsw_all_random1.csv", replace

use "nsw_all.dta", clear
set seed 42
gen sortorder = runiform()
sort sortorder
drop sortorder
export delimited using "nsw_all_random2.csv", replace

use "nsw_all.dta", clear
set seed 35456321
gen sortorder = runiform()
sort sortorder
drop sortorder
export delimited using "nsw_all_random3.csv", replace


*Export test data sets for simple propensity score regression
import delimited "nsw_all_random1.csv", case(preserve) clear
psmatch2 Treated Age, outcome(RE78) logit
export delimited using "nsw_all_random1_pscoresimple.csv", replace

import delimited "nsw_all_random2.csv", case(preserve) clear
psmatch2 Treated Age, outcome(RE78) logit
export delimited using "nsw_all_random2_pscoresimple.csv", replace

import delimited "nsw_all_random3.csv", case(preserve) clear
psmatch2 Treated Age, outcome(RE78) logit
export delimited using "nsw_all_random3_pscoresimple.csv", replace


*Export test data sets for extensive propensity score regression
import delimited "nsw_all_random1.csv", case(preserve) clear
psmatch2 Treated Age Education Black Hispanic Married Nodegree, outcome(RE78) logit
export delimited using "nsw_all_random1_pscorefull.csv", replace

import delimited "nsw_all_random2.csv", case(preserve) clear
psmatch2 Treated Age Education Black Hispanic Married Nodegree, outcome(RE78) logit
export delimited using "nsw_all_random2_pscorefull.csv", replace

import delimited "nsw_all_random3.csv", case(preserve) clear
psmatch2 Treated Age Education Black Hispanic Married Nodegree, outcome(RE78) logit
export delimited using "nsw_all_random3_pscorefull.csv", replace
