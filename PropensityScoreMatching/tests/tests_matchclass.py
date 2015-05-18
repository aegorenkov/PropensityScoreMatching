# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:30:15 2015

@author: Alexander
"""

import unittest
import PropensityScoreMatching

class MatchClass(unittest.TestCase):
    def test_match_can_initialize(self):
        match = PropensityScoreMatching.Match()
        self.assertEqual(match.match_type, 'neighbor')

class TestPropensityScoreMatchingClass(unittest.TestCase):
    pass

class TestMahalanobisMatchingClass(unittest.TestCase):
    pass

#if __name__ == '__main__':
    #unittest.main()
