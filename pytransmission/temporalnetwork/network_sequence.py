#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
import numpy as np
import networkx as nx


class NetworkSequence(object):
    """
    NetworkSequence represents a temporal network as a sequence of adjacency matrices, which represent a change
    in the state of the network at time T.  A snapshot which occurs at time T is thus valid until a new matrix
    occurs at T+m, where m is the duration between successive snapshots.  This is an "interval" network rather
    than an instantaneous event network, although high resolution change is possible as well.

    By convention, the first network state in the list should have an index of 0, and establishes the "starting state"
     of the sequence.

    The interface is designed to hide the underlying representation, and mostly pass back lists of vertices or edges
    for NetworkX graphs, and occasionally whole NetworkX graphs.
    """

    def __init__(self):
        self.time_to_matrix = {}
        self.times = []
        self.time_to_graph = {}




    def add_network(self, time, matrix):
        """
        Adds a network snapshot (in the form of an adjacency matrix) to the sequence
        :param time:
        :param matrix:
        :return:
        """
        self.time_to_matrix[time] = matrix
        self.times.append(time)
        self.times.sort()



    def get_graph_matrix_for_time(self, time):
        """
        Returns networkx Graph object for the state of the temporal network at the specified time
        :param time:
        :return:
        """
        index = None

        for t in self.times:
            if time > t:
                index = t
            elif time <= t and index != None:
                break
            else:
                continue

        # handle the zero equality case
        if time == 0:
            index = 0

        log.debug("snapshot time for index %s is: %s", time, index)

        return


    def get_new_vertices_for_time(self, time):
        """

        :param time:
        :return:
        """
        pass

    def get_removed_vertices_for_time(self, time):
        """

        :param time:
        :return:
        """
        pass


    def get_list_of_change_times(self):
        """
        Returns a list of the time indices at which network states change.  Can be used (when the graph is
        temporal but static rather than dynamic) to "schedule" polling of the network structure through the
        various get methods.  Time is always represented by an integer index, as in a discrete-time stochastic
        process (or a computational representation of a continuous time process).

        :return: list of integers
        """
        log.debug("times: %s", self.times)
        return self.times


