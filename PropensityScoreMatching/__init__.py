# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:03 2015

@author: Alexander
"""

import statsmodels.api as sm
import pandas as pd
import numpy as np

class Match(object):
    '''
    Perform matching algorithm on input data and return a list of indicies
    corresponding to matches.
    '''
    def __init__(self, match_type='neighbor'):
        self.match_type = match_type

    def match(self, treated, covariates):
        #Implement naive nearest neighbors for now
        #if treated or covariates == null raise valueError
        #if treated rows != covariate rows raise valueError
        groups = treated == treated.unique()[1]
        n = len(groups)
        n1 = groups.sum()
        n2 = n-n1
        #if n1 > n2 raise valueError
        g1, g2 = covariates[groups == 1], covariates[groups == 0]

        matches = pd.Series(np.empty(n))
        matches[:] = np.NAN

        #naive nearest neighbor for now
        for m in g1.index:
            dist = abs(g1[m]-g2) # Note this returns a vector/series
            if dist.min() <= 100: #potential set caliper later
                matches[m] = dist.argmin()
                #Implicit search..speed up with Data Structure (kd..maybe LSH)
            #g2 = g2.drop(matches[m]) replacement = false

        return matches

class PropensityScoreMatching(object):
    '''
    Propensity Score Matching in Python.
    Use psmatch2 to confirm accuracy.
    '''
    def __init__(self, model='logit'):
        self.model = model

    def fit(self, treated, design_matrix):
        '''
        Run logit or probit and return propensity score column
        '''
        link = sm.families.links.logit
        family = sm.families.Binomial(link)
        reg = sm.GLM(treated, design_matrix, family=family)
        fitted_reg = reg.fit()
        pscore = fitted_reg.fittedvalues
        self.pscore = pscore
        
#    def match(self, match_method = 'neighbor'):
#        if match_method == 'neighbor':
#            algorithm = Match(match_type = 'neighbor')
        
        

class MahalanobisMatching(object):
    '''
    Mahalanobis matching in Python.
    Use psmatch2 to confirm accuracy.
    '''
    def __init__(self):
        pass
