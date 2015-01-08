#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Description here

"""

import logging as log
import unittest
import pytransmission.temporalnetwork as tn
import numpy as np
import networkx as nx
import os
import tempfile

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

class TemporalNetworkTest(unittest.TestCase):

    def test_change_times(self):

        ns = tn.NetworkSequence()
        # complete graph on 4 vertices - could have used the networkx generator too
        t1 = np.array([[1,3,1,1],[3,1,1,1],[1,1,1,1],[1,1,1,1]])
        g = nx.to_networkx_graph(t1)

        ns.add_network(0, g)
        ns.add_network(10, g)
        ns.add_network(5, g)
        ns.add_network(25, g)
        ns.add_network(3, g)

        times = ns.get_list_of_change_times()


        ns.get_graph_matrix_for_time(8)
        ns.get_graph_matrix_for_time(12)
        ns.get_graph_matrix_for_time(0)
        ns.get_graph_matrix_for_time(50)
        ns.get_graph_matrix_for_time(1)


        self.assertTrue(True)




if __name__ == "__main__":
    unittest.main()