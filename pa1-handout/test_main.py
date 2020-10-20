import unittest
import networkx as nx
from main import *

class TestFunctions(unittest.TestCase):

    def compare_immediate_dominators(self, start, end, edges):
        G = nx.DiGraph(edges)
        idom_nx = sorted(nx.immediate_dominators(G, start).items())

        cfg = ControlFlowGraph.fromEdgeList(start, end, edges)

        dom = dominators(cfg)
        idom_hw = immediateDominator(dom)

        for node, idom in idom_nx:
            if node == start:
                self.assertEqual(idom_hw[node], '')
            else:
                self.assertEqual(idom_hw[node], idom, "nx: {}, homework: {}".format(idom_nx, idom_hw))

    def compare_dominance_frontiers(self, start, end, edges):
        G = nx.DiGraph(edges)
        dom_frontier_nx = sorted((u, sorted(df)) for u, df in nx.dominance_frontiers(G, 1).items())
        cfg = ControlFlowGraph.fromEdgeList(start, end, edges)
        
        control_nodes = findControlNodes(cfg, reverse=True)
        control_dependents = {k:[] for k in cfg.nodes}

        for controller in control_nodes:
            for controllee in control_nodes[controller]:
                if controllee == '':
                    continue
                control_dependents[controllee].append(controller)

        for node, frontiers in dom_frontier_nx:
                self.assertListEqual(sorted(control_dependents[node]), sorted(frontiers), "node: {}".format(node))

    def test_immediate_dominators(self):
        start, end = 1, 5
        edges = [(1, 2), (1, 3), (2, 5), (3, 4), (4, 5)]

        self.compare_immediate_dominators(start, end, edges)

    def test_dominance_frontiers(self):
        start, end = 1, 5
        edges = [(1, 2), (1, 3), (2, 5), (3, 4), (4, 5)]
        self.compare_dominance_frontiers(start, end, edges)



if __name__ == "__main__":
    unittest.main()