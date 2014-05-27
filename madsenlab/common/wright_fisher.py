# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""


import math
import logging as log


def expectedIAQuasiStationarityTimeHaploid(popsize,mutationrate):
    """Returns the expected time in generations for an infinite-alleles WF process to reach quasi-stationarity, as defined
        by Ewens (2004) for the "unlableled" WF-IA model.

        We use Equation 17 from Ewens and Gillespie (1974) to approximate
        this waiting time, since it seems more conservative than the estimate from Equation 9.5 from Ewens (2004).  The latter
        approximation is the mean time to lose all of the original alleles, whereas the former is the mean time for the
        leading non-unit eigenvalue of the unlabelled process to be less than or equal to 0.01, indicating a very slow rate of
        further change compared to full stationarity.

        Args:

            popsize (int): The size of the haploid population

            mutationrate (float):  the rate of innovation per individual per generation

        Returns:

            (int): The expected number of generations, rounded to the nearest integer value.

    """

    theta = 2.0 * popsize * mutationrate
    time = (9.2 * popsize) / (theta + 1.0) # this is conservative given the original constant is for the diploid process

    return int(math.ceil(time / 1000.0)) * 1000