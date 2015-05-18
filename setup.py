# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='psm',
      version='0.01',
      description="Matching methods for python",
      author='Alexander Egorenkov',
      author_email="aegorenkovcode@gmail.com",
      license='MIT',
      packages=['PropensityScoreMatching'],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)
     