# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:03 2015

@author: Alexander
"""
class Match(object):
    '''
    Perform matching algorithm on input data and return a list list of indicies
    corresponding to matches.
    '''
    def __init__(self, match_type='neighbor'):
        self.match_type = match_type

class PropensityScoreMatching(object):
    '''
    Propensity Score Matching in Python.
    Use psmatch2 to confirm accuracy.
    '''
    def __init__(self, model='logit'):
        self.model = model

class MahalanobisMatching(object):
    '''
    Mahalanobis matching in Python.
    Use psmatch2 to confirm accuracy.
    '''
    def __init__(self):
        pass
    
