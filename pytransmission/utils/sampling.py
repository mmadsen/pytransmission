#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Utility methods for sampling various objects, which is frequently done by simulations of cultural transmission

"""

import random
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
            raise Warning("sample size requested: %s is larger than population: %s" % (ssize, total))
        sample = random.sample(items, ssize)
        new_counter = Counter()
        new_counter.update(sample)
        #log.debug("counter for ssize %s: %s", ssize, new_counter)
        result[ssize] = new_counter

    return result






