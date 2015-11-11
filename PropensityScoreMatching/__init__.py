# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:03 2015

@author: Alexander
"""

from statsmodels.api import families
from statsmodels.api import GLM
import pandas as pd
import numpy as np
import sklearn.neighbors as sk

class Match(object):
    """Perform matching algorithm on input data and return a list of indicies
    corresponding to matches."""
    def __init__(self, match_type='neighbor', match_algorithm='brute'):
        self.match_type = match_type
        self.match_algorithm = match_algorithm

    @staticmethod
    def _extract_groups(treated, covariates):
        groups = treated == treated.unique()[1]
        n = len(groups)
        n1 = groups.sum()
        n2 = n-n1
        g1, g2 = covariates[groups == 1], covariates[groups == 0]
        return (g1, g2, n)

    @staticmethod
    def _naive_match(g1, g2, n):
        matches = pd.Series(np.empty(n))
        matches[:] = np.NAN

        for m in g1.index:
            # Note this returns a vector/series
            dist = abs(g1[m]-g2)
            #potential set caliper later
            if dist.min() <= 100:
                matches[m] = dist.argmin()

        return matches

    @staticmethod
    def _kd_match(g1, g2, n):
        tree = sk.KDTree([[x] for x in g2], leaf_size=1, metric='minkowski', p=2)

        matches = pd.Series(np.empty(n))
        matches[:] = np.NAN

        for m in g1.index:
            dist, ind = tree.query(g1[m], k=1, breadth_first=True)
            matches[m] = g2.index[ind[0]][0]
        return matches

    def match(self, treated, covariates):
        g1, g2, n = self._extract_groups(treated, covariates)
        if self.match_algorithm == 'brute':
            matches = self._naive_match(g1, g2, n)
        elif self.match_algorithm == 'kdtree':
            matches = self._kd_match(g1, g2, n)
        else:
            pass
        return matches


class PropensityScoreMatching(object):
    """Propensity Score Matching in Python."""
    def __init__(self, model='logit'):
        self.model = model
        self._matches = None
        self.treated = None
        self.design_matrix = None
        self.pscore = None
        self.att = None
        self.unmatched_treated_mean = None
        self.matched_treated_mean = None
        self.unmatched_control_mean = None
        self.matched_control_mean = None

    def results(self, outcome):
        """
        Recieve outcome variable and return Results object
        :param outcome: A Pandas Series or NumPy array containing outcome values
        :return: Results object
        """
        treatment = self.treated == 1
        control = self.treated == 0

        match_treatment = outcome[np.isfinite(self._matches)]
        match_control = outcome[self._matches]
        match_control = match_control[np.isfinite(match_control)]

        att = np.mean(np.subtract(match_treatment, match_control))
        self.att = att
        self.unmatched_treated_mean = np.mean(outcome[treatment])
        self.unmatched_control_mean = np.mean(outcome[control])
        self.matched_treated_mean = np.mean(match_treatment)
        self.matched_control_mean = np.mean(match_control)
        return Results()

    def fit(self, treated, design_matrix):
        """Run logit or probit and return propensity score column"""
        link = families.links.logit
        family = families.Binomial(link)
        reg = GLM(treated, design_matrix, family=family)
        fitted_reg = reg.fit()
        pscore = fitted_reg.fittedvalues
        self.treated = treated
        self.design_matrix = design_matrix
        self.pscore = pscore

    def match(self, match_method='neighbor'):
        """Take fitted propensity scores and match between treatment and
        control groups"""
        #check for valid method
        if match_method == 'neighbor':
            algorithm = Match(match_type='neighbor')
        self._matches = algorithm.match(self.treated, self.pscore)

    def get_matches(self):
        return self._matches

class MahalanobisMatching(object):
    """Mahalanobis matching in Python."""
    def __init__(self):
        pass

class Results(object):
    """
    Class to hold matching results
    """
    def __init__(self):
        pass