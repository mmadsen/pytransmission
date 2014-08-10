# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
from collections import defaultdict, Counter
from copy import deepcopy


class MoranCumulativeTimeAverager(object):
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

    def __init__(self, indextime, interval_list, popsize, numloci, ending_interval=True):
        """

        :param indextime: The simulation tick which is either the starting or ending time for the "stack" of TA intervals
        :param interval_list: A list of TA durations, given in "generations"
        :param popsize: Population size of agents, used to turn generations into clock ticks in a Moran model
        :param numloci: Number of dimensions or loci for which we're counting traits
        :param ending_interval: Boolean, indicates whether this TA interval stack is at the beginning of a survival analysis or the end.  A set of intervals not used for a dual-sample analysis should give "True" or let this default.
        :return: void

        """
        self.intervals_by_tick = [t * popsize for t in interval_list]
        self.int_tick_to_gen = dict(zip(self.intervals_by_tick, interval_list))
        self.int_gen_to_tick = dict(zip(interval_list, self.intervals_by_tick))
        self.interval_tuples = []
        self.earliest_tick = 0
        self.latest_tick = 0
        self.interval_tuple_map = dict()
        self.counts_by_interval_by_locus = dict()
        self.configurations_by_interval = dict()
        #log.debug("map intervals: %s", self.int_tick_to_gen)

        # initialize the count maps.  We use the Counter class because we can update an entire locus of counts
        # with one addition operation.  Otherwise, the intervals and loci are dicts
        for interval in self.intervals_by_tick:
            self.counts_by_interval_by_locus[interval] = defaultdict(Counter)
            self.configurations_by_interval[interval] = Counter()
            for locus in range(0,numloci):
                self.counts_by_interval_by_locus[interval][locus] = Counter()


        #log.debug("initialized count map: %s", self.counts_by_interval_by_locus)

        if ending_interval == True:
            # So we start at the indextime, and form intervals by adding each TA duration (in ticks) to it
            start = indextime
            for interval in self.intervals_by_tick:
                tup = (start, interval + start)
                self.interval_tuple_map[interval] = tup
                self.interval_tuples.append(tup)

            end_list = [t + start for t in self.intervals_by_tick]
            self.earliest_tick = indextime
            self.latest_tick = max(end_list)

        else:
            # So we start at the indextime, and form intervals by SUBTRACTING each TA duration from it
            end = indextime
            for interval in self.intervals_by_tick:
                tup = (end - interval, end)
                self.interval_tuple_map[interval] = tup
                self.interval_tuples.append(tup)


            start_list = [end - t for t in self.intervals_by_tick]
            self.earliest_tick = min(start_list)
            self.latest_tick = indextime

        #log.debug("intervals as tuples: %s", self.interval_tuples)
        #log.debug("interval tuple map: %s", self.interval_tuple_map)


    def get_interval_tuples(self):
        return self.interval_tuples

    def get_earliest_tick_for_all_intervals(self):
        return self.earliest_tick

    def get_latest_tick_for_all_intervals(self):
        return self.latest_tick

    def is_within_intervals(self, timestep):
        """
        Returns True if the timestep is within the largest of the duration intervals being tracked.

        :param timestep:
        :return: Boolean
        """
        return self.earliest_tick <= timestep <= self.latest_tick


    def _is_within_tuple(self,tup,timestep):
        return tup[0] <= timestep < tup[1]



    def record_trait_count_sample(self,timestep,countmap,configuration_map):
        """
        Given a time step, a map of trait counts by locus, and a map of counts for the cartesian product of loci (configurations),
         we iterate over the
        intervals for which we're accumulating samples.  If the timestep fits within a given
        time interval, the counts for each locus are added to those already held in the
        accumulator.  Otherwise, we move on to the next interval.

        :param timestep:
        :param countmap:
        :return:
        """

        for interval, tuple in self.interval_tuple_map.items():
            if self._is_within_tuple(tuple,timestep):
                # iterate over the loci in countmap, create a counter from the map from each locus, add that counter to the
                # main counter.  We use the addition operator because both objects are Counters, which will add the
                # counts from temp_counter to that held in the cache.

                for locus in countmap.keys():
                    counts = countmap[locus]
                    #log.debug("interval: %s before timestep %s: %s", timestep, self.counts_by_interval_by_locus[interval][locus])
                    self.counts_by_interval_by_locus[interval][locus].update(counts)
                    #log.debug("interval: %s  counts after timestep %s: %s", interval, timestep, self.counts_by_interval_by_locus[interval][locus])

                # configuration_map has the right structure to let Counter do the work
                self.configurations_by_interval[interval].update(configuration_map)

                #log.debug("configurations for interval %s: %s", interval, self.configurations_by_interval[interval])

            else:
                #log.debug("timestep %s not within interval %s", timestep, interval)
                continue


    def get_counts_for_interval_generations(self, gen):
        """
        Returns the count map for a given interval, where the interval is specified in generations.  This argument
        is turned into ticks for a Moran model, and the appropriate map of counts (by locus) is returned.

        A deep copy of the original countmap is returned, so that the caller does not accidentally modify an ongoing
        cumulative counting operation.

        :param gen:
        :return: dict of loci with Counter() instances mapping traits to counts
        """
        interval_by_tick = self.int_gen_to_tick[gen]
        countmap = self.counts_by_interval_by_locus[interval_by_tick]
        return deepcopy(countmap)


    def get_counts_all_intervals(self):
        return deepcopy(self.counts_by_interval_by_locus)


    def get_counts_for_generation_intervals(self):
        """
        Returns trait counts by locus, for each locus, for time intervals measured in generations.

        Calling code usually specifies the time averaging duration in "generations", and in moran
        dynamics this is turned into ticks internally.  For recording results, we recreate the
        count map using generations rather than ticks as keys.

        :return: dict of durations (in generations), each pointing to a dict of loci with Counter instances mapping traits to counts.
        """
        countmap_gens = dict()
        for interval, map in self.counts_by_interval_by_locus.items():
            gens = self.int_tick_to_gen[interval]
            countmap_gens[gens] = map
        return countmap_gens


    def get_configuration_counts_for_generation_intervals(self):
        """
        Return the configuration counts with generation-scale intervals instead of ticks, using the same
        method as get_counts_for_generation_intervals()

        :return: dict of durations (in generations), each pointing to a dict with configuration as key, and count as value
        """
        countmap_gens = dict()
        for interval, counter in self.configurations_by_interval.items():
            gens = self.int_tick_to_gen[interval]
            #countmap_gens[gens] = dict(counter)  # TODO only return non-zero items from the counter?
            countmap_gens[gens] = {config: count for config, count in counter.items() if count > 0}
        return countmap_gens


    def get_counts_for_generation_for_ssize_for_intervals(self, ssize_list):
        """
        Returns trait counts by locus, for each time interval in generations, for each sample size requested.
        The output is nested by interval, locus, ssize, then trait:count

        :param ssize_list:
        :return: nested dicts giving trait counts by interval, locus, and sample size
        """
        pass

    def get_configurations_for_generation_for_ssize_for_intervals(self, ssize_list):
        pass


