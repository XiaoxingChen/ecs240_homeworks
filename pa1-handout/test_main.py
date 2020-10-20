import unittest
import networkx as nx
from main import *

class TestFunctions(unittest.TestCase):

    def test_immediate_dominators(self):
        start, end = 1, 5
        edges = [(1, 2), (1, 3), (2, 5), (3, 4), (4, 5)]
        G = nx.DiGraph(edges)
        idom_nx = sorted(nx.immediate_dominators(G, start).items())

        cfg = ControlFlowGraph(len(set([node for edge in edges for node in edge ])), start, end)
        for e in edges:
            cfg.addEdge(e[0], e[1])
        dom = dominators(cfg)
        idom_hw = immediateDominator(dom)

        for node, idom in idom_nx:
            if node == start:
                self.assertEqual(idom_hw[node], '')
            else:
                self.assertEqual(idom_hw[node], idom, "node: {}, idom from nx: {}, idom from homework: {}".format(node, idom, idom_hw[node]))



if __name__ == "__main__":
    unittest.main()