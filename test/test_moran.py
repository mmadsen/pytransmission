#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@pytransmission.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
import unittest
import pytransmission.popgen.moran as moran
import os
import tempfile

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class MoranModelTest(unittest.TestCase):

    def test_basic_watkins_convergence(self):
        pop = 1000
        mutation = 0.1
        answer = 46.0517  # given by Mathematica 9

        res = moran.moran_watkins_convergence_to_stationarity(pop, mutation)
        log.debug("res: %s  answer: %s", res, answer)
        self.assertAlmostEqual(answer, res, None, None, 0.01)





if __name__ == "__main__":
    unittest.main()