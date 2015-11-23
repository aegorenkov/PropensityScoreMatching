import unittest
import PropensityScoreMatching as PSM
import pandas as pd
import numpy as np
import os

LOCAL_DIR = os.path.dirname(__file__)
FILEPATH = os.path.join('results', 'nsw_all_minimal.csv')


class TestMinimalSingle(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv(FILEPATH)
        self.outcome = self.data[u'RE78']
        self.treated = self.data[u'Treated']
        self.design_vars = [u'Age']
        self.design_matrix = self.data[self.design_vars]
        self.psm = PSM.PropensityScoreMatching()
        self.psm.fit(self.treated, self.design_matrix)
        self.psm.match()
        self.results = self.psm.results(self.outcome)

    def test_psm_should_return_correct_ATT(self):
        self.assertAlmostEquals(self.results.ATT, 1197.28503)

    def test_results_outcome_values(self):
        true_outcome = [2389.679, 17685.18, 647.20459, 6771.6221, 3523.5779, 0.,
                        0., 20893.109, 0., 0.]
        self.assertListEqual(list(self.results.outcome), list(true_outcome))

    def test_psm_should_return_correct_unmatched_treated_mean(self):
        self.assertAlmostEquals(self.results.unmatched_treated_mean, 4583.09607, 3)

    def test_psm_should_return_correct_unmatched_control_mean(self):
        self.assertAlmostEquals(self.results.unmatched_control_mean, 5596.33138, 3)

    def test_psm_should_return_correct_matched_treated_mean(self):
        self.assertAlmostEquals(self.results.matched_treated_mean, 4583.09607, 3)

    def test__should_return_correct_matched_control_mean(self):
        self.assertAlmostEquals(self.results.matched_control_mean, 3385.81104, 3)

    def psm_should_return_correct_unmatched_standard_error(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_standard_error(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_matched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_on_support(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_off_support(self):
        self.fail(msg='Not Implemented')


class TestMinimalMulti(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv(FILEPATH)
        self.outcome = self.data[u'RE78']
        self.treated = self.data[u'Treated']
        self.design_vars = [u'Age', u'Education', u'Black', u'Hispanic', u'Married', u'Nodegree']
        self.design_matrix = self.data[self.design_vars]
        self.psm = PSM.PropensityScoreMatching()
        self.psm.fit(self.treated, self.design_matrix)
        self.results = self.psm.results(self.outcome)

    def psm_should_return_correct_ATT(self):
        self.assertAlmostEquals(self.results.ATT, -11684.1557)

    def psm_should_return_correct_unmatched_treated_mean(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_control_mean(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_matched_treated_mean(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_matched_control_mean(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_standard_error(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_standard_error(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_matched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_on_support(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_off_support(self):
        self.fail(msg='Not Implemented')
