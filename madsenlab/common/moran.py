# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""


import math as math
import logging as log

def moran_watkins_convergence_to_stationarity(popsize, innovation_rate):
    """
    Returns the number of generations in the infinite-alleles Moran model before convergence to stationarity
    occurs, according to Watkins (2010) J. Math Biol 60:189-206.

    :param popsize:
    :param innovation_rate:
    :return: number of generations (units of popsize model ticks) before convergence to stationarity occurs for one locus
    """
    return math.log(popsize * innovation_rate) / innovation_rate


def moran_watkins_convergence_stationarity_timesteps(popsize, innovation_rate):
    """
    Returns the number of timesteps in the infinite-alleles Moran model for convergence to stationarity for one locus
    :param popsize:
    :param innovation_rate:
    :return: number of ticks
    """
    return popsize * moran_watkins_convergence_to_stationarity(popsize, innovation_rate)


def moran_watkins_multilocus_convergence_time_timesteps(popsize, num_loci, innovation_rate):
    """
    Under an assumption that each tick is randomly distributed among F loci, gives the number of timesteps in the
    infinite-alleles Moran model for convergence to stationarity.
    :param popsize:
    :param num_loci:
    :param innovation_rate:
    :return: number of ticks
    """
    return num_loci * moran_watkins_convergence_stationarity_timesteps(popsize, innovation_rate)