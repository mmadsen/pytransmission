#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""
import logging as log
import unittest
from collections import Counter
import pytransmission.utils as utils
import itertools

import os
import tempfile

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class SamplingTest(unittest.TestCase):

    def test_counter_sampling(self):
        test_counter = Counter()
        a = list(itertools.repeat('a', 300))
        b = list(itertools.repeat('b', 200))
        c = list(itertools.repeat('c', 400))
        test_counter.update(a)
        test_counter.update(b)
        test_counter.update(c)
        log.debug("test_counter: %s", test_counter)

        sample_sizes = [10, 50]
        for i in xrange(0,10):
            sampled = utils.get_sampled_counter(sample_sizes, test_counter)
            log.debug("results of sampling: %s", sampled)

        self.assertTrue(True)


    def test_counter_sampling_error(self):
        log.info("entering test_counter_sampling_error")
        success = False
        test_counter = Counter()
        a = list(itertools.repeat('a', 100))
        b = list(itertools.repeat('b', 100))
        c = list(itertools.repeat('c', 100))
        test_counter.update(a)
        test_counter.update(b)
        test_counter.update(c)
        log.debug("test_counter: %s", test_counter)

        sample_sizes = [10, 10000]
        for i in xrange(0,10):
            try:
                sampled = utils.get_sampled_counter(sample_sizes, test_counter)
                log.debug("results of sampling: %s", sampled)
            except Warning as w:
                log.debug("exception sample size: %s", w)
                success = True


        self.assertTrue(success)





if __name__ == "__main__":
    unittest.main()