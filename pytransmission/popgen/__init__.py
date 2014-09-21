# !/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@pytransmission.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

from moran import moran_watkins_convergence_to_stationarity, moran_watkins_convergence_stationarity_timesteps, \
    moran_watkins_multilocus_convergence_time_timesteps, moran_mutation_rate_from_theta

from wright_fisher import wfia_convergence_to_stationarity_generations


from crp import simulate_crp_memberships, get_crp_unlabeled_counts