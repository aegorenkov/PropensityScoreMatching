# -*- coding: utf-8 -*-
"""
Created on Mon May 18 15:09:03 2015

@author: Alexander
"""

from statsmodels.api import families
from statsmodels.api import GLM
from statsmodels.tools.tools import add_constant
from statsmodels.stats.weightstats import ttest_ind
import pandas as pd
import numpy as np
from collections import defaultdict


# import sklearn.neighbors as sk

def fit_reg(covariate, treated, weights=pd.Series()):
    treated = add_constant(treated)
    if not weights.any():
        reg = GLM(covariate, treated)
    else:
        reg = GLM(covariate, treated)
    res = reg.fit()
    return res


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
        n2 = n - n1
        g1, g2 = covariates[groups == 1], covariates[groups == 0]
        return (g1, g2, n)

    @staticmethod
    def _naive_match(g1, g2, n):
        matches = pd.Series(np.empty(n))
        matches[:] = np.NAN

        for m in g1.index:
            # Note this returns a vector/series
            dist = abs(g1[m] - g2)
            # potential set caliper later
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


class StatisticalMatching(object):
    """Propensity Score Matching in Python."""

    def __init__(self, method='propensity_score'):
        self.method = method
        self._matches = None
        self.treated = None
        self.design_matrix = None
        self.name = None
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

        return Results(outcome=outcome, psm=self)

    def _set_names(self, names):
        if names:
            return names
        else:
            try:
                names = list(self.design_matrix.columns)
            except AttributeError:
                raise AttributeError('No column names provided and names cannot be inferred from data.')
        return names

    def fit(self, treated, design_matrix, names=None):
        """Run logit or probit and return propensity score column"""
        link = families.links.logit
        family = families.Binomial(link)
        design_matrix = add_constant(design_matrix)
        reg = GLM(treated, design_matrix, family=family)
        fitted_reg = reg.fit()
        pscore = fitted_reg.fittedvalues

        self.fitted_reg = fitted_reg
        self.treated = treated.astype('bool')
        self.design_matrix = design_matrix
        self.names = self._set_names(names)
        self.pscore = pscore

    def match(self, match_method='neighbor'):
        """Take fitted propensity scores and match between treatment and
        control groups"""
        # check for valid method
        if self.method == 'propensity_score':
            if match_method == 'neighbor':
                algorithm = Match(match_type='neighbor')
            self._matches = algorithm.match(self.treated, self.pscore)

    @property
    def matches(self):
        return self._matches


class Results(object):
    """
    Class to hold matching results
    """

    def __init__(self, outcome, psm):
        self.outcome = outcome
        self.treated = psm.treated
        self.matches = psm.matches

    @property
    def ATT(self):
        """
        Computes the Average Treatment Effect on the Treated

        Expressed as: E[Y_{1i} - Y_{0i} | D_{i} = 1]
        Where Y is an outcome variable,
        Y_{1i} and Y_{0i} are values in the treatment and control group,
        and D is dummy of whether treatment was applied
        """
        matches = self.matches
        treatment_index = np.isfinite(matches)
        control_index = np.asarray(self.matches[np.isfinite(matches)], dtype=np.int32)

        match_treatment = self.outcome[treatment_index]
        match_control = self.outcome[control_index]

        return np.mean(np.subtract(match_treatment, match_control))

    @property
    def unmatched_treated_mean(self):
        """
        Calculates the mean of the outcome variable for observation that
        are in the treatment group
        """
        return np.mean(self.outcome[self.treated == 1])

    @property
    def unmatched_control_mean(self):
        """
        Calculates the mean of the outcome variable for observation that
        are not in the treatment group
        """
        return np.mean(self.outcome[self.treated == 0])

    @property
    def matched_treated_mean(self):
        """
        Calculates the mean of the outcome variable for treated observations
        that also have a match
        """
        has_match = np.isfinite(self.matches)
        return np.mean(self.outcome[has_match])

    @property
    def matched_control_mean(self):
        """
        Calculates the mean of the outcome variable for matched observations
        from the control group
        """
        has_match = np.isfinite(self.matches)
        match_index = np.asarray(self.matches[has_match], dtype=np.int32)
        return np.mean(self.outcome[match_index])

    @property
    def unmatched_standard_error(self):
        """
        Calculates standard error of naive treatment effect
        """
        # res = fit_reg(self.outcome, self.treated)
        # return res.bse[1]
        return (self.unmatched_treated_mean - self.unmatched_control_mean) / float(self.unmatched_t_statistic)

    @property
    def unmatched_t_statistic(self):
        """
        Calculate the t-statistics of the unmatched standard error
        """
        # return (self.unmatched_treated_mean - self.unmatched_control_mean) / float(self.unmatched_standard_error)
        treated = self.outcome[self.treated]
        controlled = self.outcome[~self.treated]
        (tstat, _, _) = ttest_ind(treated, controlled)
        return tstat

    @property
    def matched_standard_error(self):
        """
        Calculates standard error of matched treatment effect
        """

        def get_average_variance(s1, s2, n1, n2, sum_squared_weights):
            """
            Calculates the average weighted variance of the treatment and control sample

            :param s1: Treatement group variance
            :param s2: Control group variance
            :param n1: Sample size of treatment group
            :param n2: Sample size of control group
            :param sum_squared_weights: Sum squares of control observation wieghts
            :return: Returns average variance as a float
            """
            # Same as s1/float(n2) + (s2*float(sum_squared_weights))/(float(n2)**2)
            return 1 / float(n1) * s1 + float(sum_squared_weights) / (float(n1) ** 2.0) * s2

        def get_match_weights(matches):
            """
            Takes a list of match indicies and counts duplicates to determine weights
            :param matches: Pandas or numpy array representing mathes
            :return: Array of weights
            """
            weights = defaultdict(lambda: 0)
            match_indicies = matches[np.isfinite(matches)]

            for value in match_indicies:
                weights[value] += 1
            return np.asarray(weights.values())

        def sample_variance(outcomes):
            """
            Find the sample variance of a treatment or control sample
            :param outcomes: Outcome values related to a treatment or control group
            :return: Returns sample variance as a float
            """
            # Set degree of freedom as n - 1
            return np.var(outcomes, ddof=1)

        treatment_outcomes = self.outcome[self.treated]

        has_match = np.isfinite(self.matches)
        match_index = np.asarray(self.matches[has_match], dtype=np.int32)
        unique_matches = np.unique(match_index)  # don't repeat weighted obs
        control_outcomes = self.outcome[match_index[unique_matches]]

        treatment_variance = sample_variance(treatment_outcomes)
        control_variance = sample_variance(control_outcomes)

        n1, n2 = len(treatment_outcomes), len(np.unique(match_index))
        W = np.sum(get_match_weights(self.matches) ** 2)

        average_variance = get_average_variance(treatment_variance, control_variance, n1, n2, W)
        return np.sqrt(average_variance)

    @property
    def matched_t_statistic(self):
        """
        Calculate the t-statistics of the matched standard error
        """
        return (self.matched_treated_mean - self.matched_control_mean) / float(self.matched_standard_error)


class BalanceStatistics(pd.DataFrame):
    """
    Class for balance statistics from a StatisticalMatching instance as a data frame
    """

    def __init__(self, statmatch):
        """
        Populate a pandas data frame and pass it forward as BalanceStatistics
        :param statmatch: StatisticalMatching instance that has been fitted
        :return: BalanceStatistics instance
        """
        # Could be replaced with an ordered dictionary
        columns = ['unmatched_treated_mean',
                   'unmatched_control_mean',
                   'unmatched_bias',
                   'unmatched_t_statistic',
                   'unmatched_p_value',
                   'matched_treated_mean',
                   'matched_control_mean',
                   'matched_bias']

        data = {'unmatched_treated_mean': self._unmatched_treated_mean(statmatch),
                'unmatched_control_mean': self._unmatched_control_mean(statmatch),
                'unmatched_bias': self._unmatched_bias(statmatch),
                'unmatched_t_statistic': self._unmatched_t_statistic(statmatch),
                'unmatched_p_value': self._unmatched_p_value(statmatch),
                'matched_treated_mean': self._matched_treated_mean(statmatch),
                'matched_control_mean': self._matched_control_mean(statmatch),
                'matched_bias': self._matched_bias(statmatch)}

        super(BalanceStatistics, self).__init__(data, index=statmatch.names, columns=columns)
        # columns should be
        # unmatched_treated_mean, unmatched_controlled_mean, unmathced_bias, unmatched_t_test, unmatched_p_values
        # matched_treated_mean, matched_controlled_mean, matched_bias, bias_reduction, matched_t_test, matched_p_value

    def _unmatched_treated_mean(self, statmatch):
        """
        Compute the unmatched treated mean for every matching variable using vectorized operations

        Expressed as: E[X_{1i}| D_{i} = 1]

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing means for each matching variable
        """
        return np.array(statmatch.design_matrix[statmatch.names][statmatch.treated].mean())

    def _unmatched_control_mean(self, statmatch):
        """
        Compute the unmatched control mean for every matching variable using vectorized operations

        Expressed as: E[X_{1i}| D_{i} = 0]

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing means for each matching variable
        """
        return np.array(statmatch.design_matrix[statmatch.names][~statmatch.treated].mean())

    def _unmatched_bias(self, statmatch):
        """
        Compute the unmatched bias for every matching variable using vectorized operations

        Expressed as: 100 * (m1u - m0u) / sqrt((v1u + v0u) / 2)

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing normalized percent bias for each matching variable
        """
        treated_variance = np.array(statmatch.design_matrix[statmatch.names][statmatch.treated].var())
        control_variance = np.array(statmatch.design_matrix[statmatch.names][~statmatch.treated].var())
        normal = np.sqrt((treated_variance + control_variance) / 2)
        return 100 * (self._unmatched_treated_mean(statmatch) - self._unmatched_control_mean(statmatch)) / normal

    def _unmatched_t_statistic(self, statmatch):
        """
        Compute t-statistics for the difference of means test for every matching variable using vectorized operations

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing t-stats for each matching variable
        """
        treated = np.array(statmatch.design_matrix[statmatch.names][statmatch.treated])
        control = np.array(statmatch.design_matrix[statmatch.names][~statmatch.treated])
        (tstat, _, _) = ttest_ind(treated, control)
        return tstat

    def _unmatched_p_value(self, statmatch):
        """
        Compute p-values for the difference of means test for every matching variable using vectorized operations

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing t-stats for each matching variable
        """
        treated = np.array(statmatch.design_matrix[statmatch.names][statmatch.treated])
        control = np.array(statmatch.design_matrix[statmatch.names][~statmatch.treated])
        (_, pvalue, _) = ttest_ind(treated, control)
        return pvalue

    def _matched_treated_mean(self, statmatch):
        """
        Compute the matched treated mean for every matching variable using vectorized operations

        Expressed as: E[X_{2i}| D_{i} = 1]

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing means for each matching variable
        """
        has_match = np.isfinite(statmatch.matches)
        return np.array(statmatch.design_matrix[statmatch.names][has_match].mean())

    def _matched_control_mean(self, statmatch):
        """
        Compute the matched control mean for every matching variable using vectorized operations

        Expressed as: E[X_{2i}| D_{i} = 0]

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing means for each matching variable
        """
        has_match = np.isfinite(statmatch.matches)
        match_index = np.asarray(statmatch.matches[has_match], dtype=np.int32)
        return np.array(statmatch.design_matrix[statmatch.names].iloc[match_index].mean())

    def _matched_bias(self, statmatch):
        """
        Compute the matched bias for every matching variable using vectorized operations

        Expressed as: 100 * (m1m - m0m) / sqrt((v1m + v0m) / 2)

        :param statmatch: StatisticalMatching instance that has been fitted
        :return: NumPy array containing normalized percent bias for each matching variable
        """
        treated_variance = np.array(statmatch.design_matrix[statmatch.names][statmatch.treated].var())
        control_variance = np.array(statmatch.design_matrix[statmatch.names][~statmatch.treated].var())

        normal = np.sqrt((treated_variance + control_variance) / 2)

        return 100 * (self._matched_treated_mean(statmatch) - self._matched_control_mean(statmatch)) / normal
