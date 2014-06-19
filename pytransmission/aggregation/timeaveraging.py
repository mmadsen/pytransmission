# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log


class MoranTimeAverager(object):
    """
    Tracks one set of time averaged trait counts, over a set of intervals.  Given a Moran model,
    the intervals are given in "generations" -- number of cycles through N individuals.  The class
    translates this into simulation ticks internally given population size.

    In order to facilitate comparison of time averaged samples which are separated by specific interval
    which needs to be constant across comparisons (e.g., Kandler and Shennan's trait survival analysis),
    we build a stack of nested intervals.  A "starting" interval stacks the nested intervals up from the
    final time index of the whole set -- i.e., the ending tick of each interval is the same, but the
    beginning tick of each interval varies.  An "ending" interval stacks nested intervals from the initial
    time index of the whole set -- i.e., the starting tick of each interval is the same, but the ending
    tick varies.  A starting interval is specified by giving "ending_interval = False", while an ending
    interval is "True."

    """

    def __init__(self, indextime, interval_list, popsize, ending_interval=True):
        """

        :param indextime: The simulation tick which is either the starting or ending time for the "stack" of TA intervals
        :param interval_list: A list of TA durations, given in "generations"
        :param popsize: Population size of agents, used to turn generations into clock ticks in a Moran model
        :param ending_interval: Boolean, indicates whether this TA interval stack is at the beginning of a survival analysis or the end.  A set of intervals not used for a dual-sample analysis should give "True" or let this default.
        :return: void

        """
        self.intervals_by_tick = [t * popsize for t in interval_list]
        self.interval_tuples = []
        self.earliest_tick = 0
        self.latest_tick = 0

        if ending_interval == True:
            # So we start at the indextime, and form intervals by adding each TA duration (in ticks) to it
            start = indextime
            end_list = [t + start for t in self.intervals_by_tick]
            for end in end_list:
                self.interval_tuples.append((start, end))

            self.earliest_tick = indextime
            self.latest_tick = max(end_list)

        else:
            # So we start at the indextime, and form intervals by SUBTRACTING each TA duration from it
            end = indextime
            start_list = [end - t for t in self.intervals_by_tick]

            for start in start_list:
                self.interval_tuples.append((start,end))

            self.earliest_tick = min(start_list)
            self.latest_tick = indextime

        log.debug("intervals as tuples: %s", self.interval_tuples)


    def get_interval_tuples(self):
        return self.interval_tuples

    def get_earliest_tick_for_all_intervals(self):
        return self.earliest_tick

    def get_latest_tick_for_all_intervals(self):
        return self.latest_tick

    def is_within_intervals(self, timestep):
        return self.earliest_tick <= timestep <= self.latest_tick


    def record_sample(self,pop):
        pass
