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
FILENAMES = [r'results/nsw_all_random1_pscoresimple.csv',
             r'results/nsw_all_random2_pscoresimple.csv',
             r'results/nsw_all_random3_pscoresimple.csv']
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

    def test_set1_matches_in_order(self):
        testdata = DATASET1.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == DATASET1["_n1"]))

    def test_set2_matches_in_order(self):
        testdata = DATASET2.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == DATASET2["_n1"]))

    def test_set3_matches_in_order(self):
        testdata = DATASET3.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == DATASET3["_n1"]))

class PropensityScoreMatchingClass(unittest.TestCase):
    #We don't define setUp because we will need to change parameters of the
    #psm instance
    def test_psm_can_initialize(self):
        psm = PSM.PropensityScoreMatching()
        self.assertEqual(psm.model, 'logit')

    def test_set1_pscores_should_equal_data_pscores(self):
        treated = DATASET1['Treated']
        design_matrix = DATASET1['Age']
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = DATASET1['_pscore']
        ss_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(ss_diff, 0)

    def test_set2_pscores_should_equal_data_pscores(self):
        treated = DATASET2['Treated']
        design_matrix = DATASET2['Age']
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = DATASET2['_pscore']
        ss_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(ss_diff, 0)

    def test_set3_pscores_should_equal_data_pscores(self):
        treated = DATASET3['Treated']
        design_matrix = DATASET3['Age']
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = DATASET3['_pscore']
        ss_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(ss_diff, 0)

class TestMahalanobisMatchingClass(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
