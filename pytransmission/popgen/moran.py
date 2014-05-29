# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@pytransmission.org>
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


def moran_mutation_rate_from_theta(popsize, theta):
    """
    Given a value for theta (the population-level dimensionless innovation rate, returns the actual probability
    of mutation per clock tick given Equation 3.98 from Ewens 2004.  This is a *per locus* innovation rate, however,
    so if you are using this in code which randomly selects one of M loci to receive a mutation, then you should use
    M * mutation_rate to determine the actual probability of an event happening in a timestep.

    theta = 2 * popsize * mutation / (1 - mutation)

    mutation is thus (theta / 2N) / (1 - theta / 2N)

    :param popsize:
    :param theta:
    :return:
    """
    intermediate = float(theta) / ( 2.0 * float(popsize))

    mutation = intermediate / (1.0 - intermediate)
    #log.debug("mutation rate from N: %s and theta: %s:  %s", popsize, theta, mutation)
    return mutation
