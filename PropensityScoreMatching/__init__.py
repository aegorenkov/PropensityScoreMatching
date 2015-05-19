# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:03 2015

@author: Alexander
"""
class Match(object):
    '''
    Perform matching algorithm on input data and return a list of indicies
    corresponding to matches.
    '''
    def __init__(self, match_type='neighbor'):
        self.match_type = match_type

    def match(self, covariates):
        pass

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
        pass

class MahalanobisMatching(object):
    '''
    Mahalanobis matching in Python.
    Use psmatch2 to confirm accuracy.
    '''
    def __init__(self):
        pass
