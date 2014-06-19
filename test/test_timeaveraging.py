#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@pytransmission.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
import unittest
import pytransmission.popgen.moran as m
import pytransmission.aggregation as agg
import os
import tempfile

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class MoranTimeAveragingTest(unittest.TestCase):

    def test_starting_interval_initialization(self):
        log.info("test_starting_interval_initialization")
        popsize = 100
        intervals = [10,50,100]
        # expected given in ticks from 100K
        expected = [(99000, 100000), (95000, 100000), (90000, 100000)]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,ending_interval=False)
        obs = tatrack.get_interval_tuples()
        self.assertEqual(expected,obs)



    def test_ending_interval_initialization(self):
        log.info("test_ending_interval_initialization")
        popsize = 100
        intervals = [10,50,100]
        # expected given in ticks from 100K
        expected = [(100000, 101000), (100000, 105000), (100000, 110000)]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,ending_interval=True)
        obs = tatrack.get_interval_tuples()
        self.assertEqual(expected,obs)


    def test_in_interval(self):
        log.info("test_in_interval")
        popsize = 100
        intervals = [10,50,100]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,ending_interval=True)

        # this should return true
        timestep = 103501

        log.debug("earliest: %s  latest: %s  step: %s", tatrack.get_earliest_tick_for_all_intervals(), tatrack.get_latest_tick_for_all_intervals(), timestep)

        obs = tatrack.is_within_intervals(timestep)
        self.assertTrue(obs)







if __name__ == "__main__":
    unittest.main()