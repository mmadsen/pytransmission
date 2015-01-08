#!/usr/bin/env python
# Copyright (c) 2015.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
import unittest
import pytransmission.popgen.wright_fisher as wf
import os
import tempfile

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class WrightFisherTest(unittest.TestCase):


    def test_mutation_from_theta(self):
        theta = [0.25, 0.5, 1.0, 2.0, 3.0, 10.0]
        popsize = 100

        for t in theta:
            mut = wf.wf_mutation_rate_from_theta(popsize, t)

        self.assertTrue(True,"Not a full test, always passes")


if __name__ == "__main__":
    unittest.main()