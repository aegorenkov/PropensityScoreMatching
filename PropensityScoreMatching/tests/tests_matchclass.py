# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:30:15 2015

@author: Alexander
"""

import unittest
import PropensityScoreMatching as PSM
import pandas as pd
import numpy as np
import os
LOCAL_DIR = os.path.dirname(__file__)
FILENAMES = [os.path.join('results', 'nsw_all_random1_pscoresimple.csv'),
             os.path.join('results', 'nsw_all_random2_pscoresimple.csv'),
             os.path.join('results', 'nsw_all_random3_pscoresimple.csv')]
FILEPATHS = [os.path.join(LOCAL_DIR, name) for name in FILENAMES]

DATASET1 = pd.read_csv(FILEPATHS[0])
DATASET2 = pd.read_csv(FILEPATHS[1])
DATASET3 = pd.read_csv(FILEPATHS[2])

class MatchClass(unittest.TestCase):
    #We don't define setUp because we will need to change parameters of the
    #match instance
    def test_match_can_initialize(self):
        match = PSM.Match()
        self.assertEqual(match.match_type, 'neighbor')

    def test_set1_idlist_is_same_length_as_data(self):
        testdata = DATASET1.sort(columns="_id", )
        match = PSM.Match()
        id_list = match.match(testdata["Treated"], testdata["_pscore"])
        self.assertTrue(len(id_list) == len(DATASET1["_n1"]),
                        msg="List of matches has incorrect length")

    def test_set1_matches_in_order(self):
        testdata = DATASET1
        match = PSM.Match()
        id_list = match.match(testdata["Treated"], testdata["_pscore"])
        test_list, true_list = testdata["_id"][id_list], testdata["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)
        #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

    def test_set2_matches_in_order(self):
        testdata = DATASET2
        match = PSM.Match()
        id_list = match.match(testdata["Treated"], testdata["_pscore"])
        test_list, true_list = testdata["_id"][id_list], testdata["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)
        #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

    def test_set3_matches_in_order(self):
        testdata = DATASET3
        match = PSM.Match()
        id_list = match.match(testdata["Treated"], testdata["_pscore"])
        test_list, true_list = testdata["_id"][id_list], testdata["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)
        #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

class PropensityScoreMatchingClass(unittest.TestCase):
    #We don't define setUp because we will need to change parameters of the
    #psm instance
    @staticmethod
    def load_data(dataset, key_range):
        treated = dataset['Treated']
        names = dataset.keys()[key_range]
        design_matrix = dataset[names]
        design_matrix['Intercept'] = 1
        return (treated, design_matrix)

    def test_psm_can_initialize(self):
        psm = PSM.StatisticalMatching()
        self.assertEqual(psm.model, 'logit')

    def test_set1_pscores_should_equal_data_pscores(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        pscore_fit = psm.pscore
        pscore_actual = DATASET1['_pscore']
        mean_diff = np.mean(np.abs(pscore_fit-pscore_actual))
        self.assertAlmostEqual(mean_diff, 0)

    def test_set2_pscores_should_equal_data_pscores(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        pscore_fit = psm.pscore
        pscore_actual = DATASET2['_pscore']
        mean_diff = np.mean(np.abs(pscore_fit-pscore_actual))
        self.assertAlmostEqual(mean_diff, 0)

    def test_set3_pscores_should_equal_data_pscores(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        pscore_fit = psm.pscore
        pscore_actual = DATASET3['_pscore']
        mean_diff = np.mean(np.abs(pscore_fit-pscore_actual))
        self.assertAlmostEqual(mean_diff, 0)

    def test_set1_matches_should_equal_actual_matches(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()

        id_list = psm.matches
        test_list, true_list = DATASET1["_id"][id_list], DATASET1["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)

            #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

    def test_set2_matches_should_equal_actual_matches(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()

        id_list = psm.matches
        test_list, true_list = DATASET2["_id"][id_list], DATASET2["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)

        #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

    def test_set3_matches_should_equal_actual_matches(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        id_list = psm.matches
        test_list, true_list = DATASET3["_id"][id_list], DATASET3["_n1"]
        #Raise assertionError if id_list cannot match the order if id and n1
        np.testing.assert_array_equal(test_list, true_list)

        #Explicitly test matching without nan values
        test_list = test_list[np.isfinite(test_list)]
        true_list = true_list[np.isfinite(true_list)]
        self.assertTrue(np.array_equal(test_list, true_list))

    def test_set1_unmatched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET1['RE78'])
        res = psm.unmatched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set1_matched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET1['RE78'])
        res = psm.matched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set1_unmatched_control_mean_should_equal_4554(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET1['RE78'])
        res = psm.unmatched_control_mean
        self.assertAlmostEqual(res, 4554.80112, places=4)

    def test_set1_matched_control_mean_should_equal_5341(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET1['RE78'])
        res = psm.matched_control_mean
        self.assertAlmostEqual(res, 5341.43016, places=4)

    def test_set1_ATT_should_equal_1007(self):
        treated, design_matrix = self.load_data(DATASET1, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET1['RE78'])
        res = psm.att
        self.assertAlmostEqual(res, 1007.71335, places=4)

    def test_set2_unmatched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET2['RE78'])
        res = psm.unmatched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set2_matched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET2['RE78'])
        res = psm.matched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set2_unmatched_control_mean_should_equal_4554(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET2['RE78'])
        res = psm.unmatched_control_mean
        self.assertAlmostEqual(res, 4554.80112, places=4)

    def test_set2_matched_control_mean_should_equal_3397(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET2['RE78'])
        res = psm.matched_control_mean
        self.assertAlmostEqual(res, 3397.68807, places=4)

    def test_set2_ATT_should_equal_2951(self):
        treated, design_matrix = self.load_data(DATASET2, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET2['RE78'])
        res = psm.att
        self.assertAlmostEqual(res, 2951.45543, places=4)

    def test_set3_unmatched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET3['RE78'])
        res = psm.unmatched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set3_matched_treated_mean_should_equal_6349(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET3['RE78'])
        res = psm.matched_treated_mean
        self.assertAlmostEqual(res, 6349.1435, places=4)

    def test_set3_unmatched_control_mean_should_equal_4554(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET3['RE78'])
        res = psm.unmatched_control_mean
        self.assertAlmostEqual(res, 4554.80112, places=4)

    def test_set3_matched_control_mean_should_equal_4148(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET3['RE78'])
        res = psm.matched_control_mean
        self.assertAlmostEqual(res, 4148.65249, places=4)

    def test_set3_ATT_should_equal_2200(self):
        treated, design_matrix = self.load_data(DATASET3, [1])
        psm = PSM.StatisticalMatching()
        psm.fit(treated, design_matrix)
        psm.match()
        psm.results(DATASET3['RE78'])
        res = psm.att
        self.assertAlmostEqual(res, 2200.49101, places=4)

class TestMahalanobisMatchingClass(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
