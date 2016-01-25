import unittest
import PropensityScoreMatching as PSM
import pandas as pd
import os

LOCAL_DIR = os.path.dirname(__file__)


class TestMinimalSingle(unittest.TestCase):
    def setUp(self):
        filepath = os.path.join('results', 'nsw_all_minimal_pscoresimple.csv')
        self.data = pd.read_csv(filepath)
        self.outcome = self.data[u'RE78']
        self.treated = self.data[u'Treated']
        self.design_vars = [u'Age']
        self.design_matrix = self.data[self.design_vars]
        self.psm = PSM.StatisticalMatching()
        self.psm.fit(self.treated, self.design_matrix, names=self.design_vars)
        self.psm.match()
        self.results = self.psm.results(self.outcome)

    def test_psm_should_contain_column_names(self):
        self.assertEqual(self.psm.names, [u'Age'])

    def psm_should_return_correct_ATT(self):
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

    def should_return_correct_matched_control_mean(self):
        self.assertAlmostEquals(self.results.matched_control_mean, 3385.81104, 3)

    def psm_should_return_correct_unmatched_standard_error(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_unmatched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_matched_t_statistic(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_on_support(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_off_support(self):
        self.fail(msg='Not Implemented')


class TestMinimalAgeEducation(unittest.TestCase):
    def setUp(self):
        filepath = os.path.join('results', 'nsw_all_minimal_pscore_age_education.csv')
        self.data = pd.read_csv(filepath)
        self.outcome = self.data[u'RE78']
        self.treated = self.data[u'Treated']
        self.design_vars = [u'Age', u'Education']
        self.design_matrix = self.data[self.design_vars]
        self.psm = PSM.StatisticalMatching()
        self.psm.fit(self.treated, self.design_matrix, names=self.design_vars)
        self.psm.match()
        self.results = self.psm.results(self.outcome)

    def test_psm_should_contain_column_names(self):
        self.assertEqual(self.psm.names, [u'Age', u'Education'])

    def test_psm_should_return_correct_ATT(self):
        self.assertAlmostEquals(self.results.ATT, -1093.04022, 3)

    def test_psm_should_return_correct_unmatched_treated_mean(self):
        self.assertAlmostEquals(self.results.unmatched_treated_mean, 4583.09607, 3)

    def test_psm_should_return_correct_unmatched_control_mean(self):
        self.assertAlmostEquals(self.results.unmatched_control_mean, 5596.33138, 3)

    def test_psm_should_return_correct_matched_treated_mean(self):
        self.assertAlmostEquals(self.results.matched_treated_mean, 4583.09607, 3)

    def test_psm_should_return_correct_matched_control_mean(self):
        self.assertAlmostEquals(self.results.matched_control_mean, 5676.13629, 3)

    def test_psm_should_return_correct_unmatched_standard_error(self):
        self.assertAlmostEquals(self.results.unmatched_standard_error, 5311.91113, 3)

    def test_psm_should_return_correct_unmatched_t_statistic(self):
        self.assertAlmostEqual(self.results.unmatched_t_statistic, -0.19, 2)

    def test_psm_should_return_correct_matched_standard_error(self):
        self.assertAlmostEqual(self.results.matched_standard_error, 5009.74651, 3)

    def test_psm_should_return_correct_matched_t_statistic(self):
        self.assertAlmostEqual(self.results.matched_t_statistic, -0.22, 2)

    def psm_should_return_correct_observations_on_support(self):
        self.fail(msg='Not Implemented')

    def psm_should_return_correct_observations_off_support(self):
        self.fail(msg='Not Implemented')


class TestMinimalAgeEducationBalanceStatistics(unittest.TestCase):
    def setUp(self):
        filepath = os.path.join('results', 'nsw_all_minimal_pscore_age_education.csv')
        self.data = pd.read_csv(filepath)
        self.outcome = self.data[u'RE78']
        self.treated = self.data[u'Treated']
        self.design_vars = [u'Age', u'Education']
        self.design_matrix = self.data[self.design_vars]
        self.psm = PSM.StatisticalMatching()
        self.psm.fit(self.treated, self.design_matrix, names=self.design_vars)
        self.psm.match()
        self.balance_statistics = PSM.BalanceStatistics(self.psm)

    def test_unmatched_treated_means_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_treated_mean['Age'], 34, 2)
        self.assertAlmostEqual(self.balance_statistics.unmatched_treated_mean['Education'], 10.5, 2)

    def test_unmatched_controlled_means_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_control_mean['Age'], 22.5, 2)
        self.assertAlmostEqual(self.balance_statistics.unmatched_control_mean['Education'], 10, 2)

    def test_unmatched_percent_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_bias['Age'], 111.0, 0)
        self.assertAlmostEqual(self.balance_statistics.unmatched_bias['Education'], 25.5, 0)

    def test_unmatched_t_statistic_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_t_statistic['Age'], 1.94, 2)
        self.assertAlmostEqual(self.balance_statistics.unmatched_t_statistic['Education'], 0.42, 2)

    def test_unmatched_p_value_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_p_value['Age'], 0.089, 3)
        self.assertAlmostEqual(self.balance_statistics.unmatched_p_value['Education'], 0.684, 3)

    def test_matched_treated_means_should_be_correct(self):
        # This needs to be separate from unmatched means in case
        # we use a matching procedure that eliminates treatment observation
        self.assertAlmostEqual(self.balance_statistics.matched_treated_mean['Age'], 34, 2)
        self.assertAlmostEqual(self.balance_statistics.matched_treated_mean['Education'], 10.5, 2)

    def test_matched_control_means_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_control_mean['Age'], 25.5, 2)
        self.assertAlmostEqual(self.balance_statistics.matched_control_mean['Education'], 10.5, 2)

    def test_matched_percent_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_bias['Age'], 82.0, 0)
        self.assertAlmostEqual(self.balance_statistics.matched_bias['Education'], 0.0, 0)

    def test_matched_t_statistic_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_t_statistic['Age'], 1.14, 2)
        self.assertAlmostEqual(self.balance_statistics.matched_t_statistic['Education'], 0.00, 2)

    def test_matched_p_value_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_p_value['Age'], 0.298, 3)
        self.assertAlmostEqual(self.balance_statistics.matched_p_value['Education'], 1.000, 3)

    def test_bias_reduction_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.bias_reduction['Age'], 26.1, 1)
        self.assertAlmostEqual(self.balance_statistics.bias_reduction['Education'], 100.0, 1)

    def test_unmatched_mean_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_mean_bias, 68.3, 1)

    def test_matched_mean_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_mean_bias, 41.0, 1)

    def test_unmatched_median_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_median_bias, 68.3, 1)

    def test_matched_median_bias_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_median_bias, 41.0, 1)

    def test_unmatched_pseudo_r2_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_prsquared, 0.266, 2)

    def test_unmatched_likelihood_ratio_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_llr, 3.58, 2)

    def test_unmatched_likelihood_ratio_pvalue_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.unmatched_llr_pvalue, 0.167, 2)

    def test_matched_pseudo_r2_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_prsquared, 0.150, 2)

    def test_matched_likelihood_ratio_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_llr, 1.66, 2)

    def test_matched_likelihood_ratio_pvalue_should_be_correct(self):
        self.assertAlmostEqual(self.balance_statistics.matched_llr_pvalue, 0.436, 2)


class TestFitReg(unittest.TestCase):
    def test_fit_reg_should_solve(self):
        covariate = [[2389.67900], [17685.18000], [647.20459], [6771.62210], [3523.57790], [0.00000], [0.00000],
                     [20893.10900],
                     [0.00000], [0.00000]]
        treated = [False, True, True, False, False, False, True, False, True, False]
        treated = [[0], [1], [1], [0], [0], [0], [1], [0], [1], [0]]
        res = PSM.fit_reg(covariate, treated)


class TestRosenbaumBounds(unittest.TestCase):
    def setUp(self):
        # filepath = os.path.join('results', 'nsw_all_minimal_pscore_age_education.csv')
        # self.data = pd.read_csv(filepath)
        # self.outcome = self.data[u'Black']
        # self.treated = self.data[u'Treated']
        # self.design_vars = [u'Age', u'Education']
        # self.design_matrix = self.data[self.design_vars]
        # self.psm = PSM.StatisticalMatching()
        # self.psm.fit(self.treated, self.design_matrix, names=self.design_vars)
        # self.psm.match()
        self.bounds = PSM.RosenbaumBounds()

    def test_expected_successes_gamma_1(self):
        self.assertEqual(self.bounds._expected_successes(1, 'upper', 6.0, 4.0, 7.0), None)

    def test_expected_successes(self):
        self.assertEqual(self.bounds._expected_successes(1.2, 'upper', 6.0, 4.0, 7.0), 3.4671336893257196)

    def test_q_mh_plus_1(self):
        self.assertAlmostEqual(self.bounds.q_mh_plus(gamma=1), 0.144338, 5)

    def test_q_mh_plus_1_2(self):
        self.assertAlmostEqual(self.bounds.q_mh_plus(gamma=1.2), 0.071257, 5)

    def test_q_mh_minus_1(self):
        self.assertAlmostEqual(self.bounds.q_mh_minus(gamma=1), 0.144338, 5)

    def test_q_mh_minus_1_2(self):
        self.assertAlmostEqual(self.bounds.q_mh_minus(gamma=1.2), 0.24138, 5)
