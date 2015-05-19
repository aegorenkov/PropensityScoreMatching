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
SET1 = pd.read_csv(FILEPATHS[0])
SET2 = pd.read_csv(FILEPATHS[1])
SET3 = pd.read_csv(FILEPATHS[2])

class MatchClass(unittest.TestCase):
    def test_match_can_initialize(self):
        match = PSM.Match()
        self.assertEqual(match.match_type, 'neighbor')

    def test_set1_matches_in_order(self):
        testdata = SET1.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == SET1["_n1"]))

    def test_set2_matches_in_order(self):
        testdata = SET2.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == SET2["_n1"]))

    def test_set3_matches_in_order(self):
        testdata = SET3.sort(columns="_id")
        match = PSM.Match()
        id_list = match.match(testdata)
        self.assertTrue(all(id_list == SET3["_n1"]))

class PropensityScoreMatchingClass(unittest.TestCase):
    #We don't define setUp because we will need to change parameters of the 
    #psm instance
    def test_PSM_can_initialize(self):
        psm = PSM.PropensityScoreMatching()
        self.assertEqual(psm.model, 'logit')
    
    def test_set1_pscores_should_equal_data_pscores(self):
        treated = SET1.Treated
        design_matrix = SET1.Age
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = SET1._pscore
        SS_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(SS_diff, 0)
    
    def test_set2_pscores_should_equal_data_pscores(self):
        treated = SET2.Treated
        design_matrix = SET2.Age
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = SET2._pscore
        SS_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(SS_diff, 0)
    
    def test_set3_pscores_should_equal_data_pscores(self):
        treated = SET3.Treated
        design_matrix = SET3.Age
        psm = PSM.PropensityScoreMatching()
        pscore_fit = psm.fit(treated, design_matrix)
        pscore_actual = SET3._pscore
        SS_diff = np.sum((pscore_fit-pscore_actual)**2)
        self.assertAlmostEqual(SS_diff, 0)

class TestMahalanobisMatchingClass(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
