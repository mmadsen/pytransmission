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
        numloci = 2
        intervals = [10,50,100]
        # expected given in ticks from 100K
        expected = [(99000, 100000), (95000, 100000), (90000, 100000)]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,numloci,ending_interval=False)
        obs = tatrack.get_interval_tuples()
        self.assertEqual(expected,obs)



    def test_ending_interval_initialization(self):
        log.info("test_ending_interval_initialization")
        popsize = 100
        numloci = 2
        intervals = [10,50,100]
        # expected given in ticks from 100K
        expected = [(100000, 101000), (100000, 105000), (100000, 110000)]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,numloci,ending_interval=True)
        obs = tatrack.get_interval_tuples()
        self.assertEqual(expected,obs)


    def test_in_interval(self):
        log.info("test_in_interval")
        popsize = 100
        numloci = 2
        intervals = [10,50,100]
        tatrack = agg.MoranTimeAverager(100000,intervals,popsize,numloci,ending_interval=True)

        # this should return true
        timestep = 103501

        log.debug("earliest: %s  latest: %s  step: %s", tatrack.get_earliest_tick_for_all_intervals(), tatrack.get_latest_tick_for_all_intervals(), timestep)

        obs = tatrack.is_within_intervals(timestep)
        self.assertTrue(obs)


    def test_add_counts_onelocus(self):
        log.info("test_add_counts_onelocus - adding two sets of counts.  The first set fits in both intervals, the second only in the second interval")
        popsize = 100
        numloci = 1
        intervals = [10,50]
        tatrack = agg.MoranTimeAverager(10000,intervals,popsize,numloci,ending_interval=True)

        timestep = 10025
        countmap = dict()
        counts = {1001: 5, 1002: 15, 1009: 9, 1011: 1}
        countmap[0] = counts

        tatrack.record_trait_count_sample(timestep, countmap)

        timestep = 11005
        countmap = dict()
        counts = {1001: 5, 1002: 15, 1009: 9, 1011: 1}
        countmap[0] = counts

        tatrack.record_trait_count_sample(timestep, countmap)

        countmap_10 = tatrack.get_counts_for_interval_generations(10)
        countmap_50 = tatrack.get_counts_for_interval_generations(50)

        count_10_1002 = countmap_10[0][1002]
        count_50_1002 = countmap_50[0][1002]

        log.debug("trait 1002 - interval 10: %s interval 50: %s", count_10_1002, count_50_1002 )

        log.debug("all counts: %s", tatrack.get_counts_all_intervals())

        self.assertEqual(count_50_1002, 30)
        self.assertEqual(count_10_1002, 15)





if __name__ == "__main__":
    unittest.main()