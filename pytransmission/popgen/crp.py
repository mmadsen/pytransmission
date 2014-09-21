# Simulation of the Chinese Restaurant Process, which is equivalent to the Ewens Sampling Distribution
# under some parameterizations.

import numpy as np
import random as rand
import logging as log

# RUBY code to translate....

# def chinese_restaurant_process(num_customers, alpha)
#    return [] if num_customers <= 0
#
#    table_assignments = [1] # first customer sits at table 1
#    next_open_table = 2 # index of the next empty table
#
#    # Now generate table assignments for the rest of the customers.
#    1.upto(num_customers - 1) do |i|
#      if rand < alpha.to_f / (alpha + i)
#        # Customer sits at new table.
#        table_assignments << next_open_table
#        next_open_table += 1
#      else
#        # Customer sits at an existing table.
#        # He chooses which table to sit at by giving equal weight to each
#        # customer already sitting at a table.
#        which_table = table_assignments[rand(table_assignments.size)]
#        table_assignments << which_table
#      end
#    end
#
#    table_assignments
# end

def simulate_crp_memberships(population, theta):
    """
    Simulates the Chinese Restaurant Process with alpha = 0, theta representing the
    probability that a new "table" is added at a given step (i.e., mutation/innovation).
    Confusingly, in a lot of pure math or Bayesian nonparametric contexts, this parameter
    is referred to as "alpha", with theta being the "discount" parameter in a two parameter
    generalized Pitman process.

    This method returns a list of len(population) with the table/trait assignments for each
    individual.

    :param population:
    :param theta:
    :return: list of individual table/trait assignments
    """
    theta_f = float(theta)
    if population < 1:
        raise UserWarning("Population size must be positive for calculating CRP partitions")

    assignments = []
    current_slot = 1
    assignments.append(current_slot)  # first individual assigned to slot 1
    for i in xrange(2, population):
        prob = theta_f / (i - 1 + theta_f)
        if np.random.random_sample() < prob:
            # assign individual to a new slot
            current_slot += 1
            #log.debug("individual %s assigned to new slot %s", i, next_slot)
            assignments.append(current_slot)
        else:
            # individual gets an existing slot
            slot = rand.choice(assignments)
            #log.debug("individual %s assigned to existing slot %s", i, slot)
            assignments.append(slot)

    return assignments


def get_crp_unlabeled_counts(population, theta):
    """
    Simulates the Chinese Restaurant Process using simulate_crp_memberships(),
    and returns unlabeled trait counts, sorted from largest to smallest.

    :param population:
    :param theta:
    :return: list of unlabeled counts
    """
    return sorted(np.bincount(simulate_crp_memberships(population, theta))[1:], reverse=True,key=int)


