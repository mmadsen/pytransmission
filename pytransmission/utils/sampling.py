#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Utility methods for sampling various objects, which is frequently done by simulations of cultural transmission

"""

import random
import numpy.random as npr
from collections import Counter
import logging as log


def get_sampled_counter(ssize_list, counter):
    """
    Given a Counter object, and one or more sample sizes, take samples from the Counter
    of the appropriate sizes, creating new Counter objects with those samples.  Return
    a dict with the requested ssize as key, and the new sampled Counter objects as values.

    :param ssize_list:
    :param counter:
    :return: dict with { ssize: counter } for all ssize in ssize_list
    """
    result = dict()
    # unpacks the counts into a list, so {trait1:3, trait2:2} becomes {trait1,trait1,trait1,trait2,trait2}
    items = list(counter.elements())
    total = sum(counter.values())
    #log.debug("total represented in counter: %s", total)
    #log.debug("original Counter: %s", counter)
    for ssize in ssize_list:
        if ssize > total:
            raise ValueError("sample size requested: %s is larger than population: %s" % (ssize, total))
        sample = random.sample(items, ssize)
        new_counter = Counter()
        new_counter.update(sample)
        #log.debug("counter for ssize %s: %s", ssize, new_counter)
        result[ssize] = new_counter

    return result


def get_sampled_dict_counts(ssize_list, dcounts):
    """
    Often, we use a dict to keep counts of categories, classes, traits.  Given a dict where
    objects to count are keys, and counts are values, take samples from the dict with sizes
    given in the ssize_list, and return a new dict with the requested ssize as key, and a dict with
    object:count_in_sample as value.

    :param ssize_list:
    :param dcounts:
    :return: dict with { ssize: { object: count }} for all ssize in ssize_list
    """
    result = dict()
    total = sum(dcounts.values())
    for ssize in ssize_list:
        if ssize > total:
            raise ValueError("sample size requested: %s is larger than the population: %s" % (ssize, total))

        traits = []
        prob = []
        for trait, count in dcounts.items():
            traits.append(trait)
            prob.append(float(count) / float(total))

        sampled_counts = npr.multinomial(ssize,prob,size=1)
        count_list = sampled_counts.tolist()
        #log.debug("traits: %s total: %s prob: %s counts: %s", traits, total, prob, count_list)
        sampled_dict = dict(zip(traits, count_list[0]))
        result[ssize] = sampled_dict

    #log.debug("result from sampled dict: %s", result)
    return result







