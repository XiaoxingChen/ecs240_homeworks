import unittest
import networkx as nx
from main import *

def generateGraphList():
    graphs = []
    graphs.append({'start':1, 'end':5, 'edges': [(1, 2), (1, 3), (2, 5), (3, 4), (4, 5)]})
    graphs.append({'start':5, 'end':6, 'edges': [(5,4), (5,3), (4,1), (3,2), (1,2), (2,1), (1,6)]})
    graphs.append({'start':1, 'end':8, 'edges': [(1,2), (2,3),(3,4), (4,7), (3,5), (5,6),(6,7), (7,2), (6,5), (2,8)]})
    graphs.append({'start':1, 'end':6, 'edges': [(1,2), (2,3), (3,4), (3,5), (4,5), (5,2), (2,6)]})

    graphs_reverse = []
    for g in graphs:
        graphs_reverse.append({'start':g['end'], 'end': g['start'], 'edges': [(e[1], e[0]) for e in g['edges']]})
     
    return graphs + graphs_reverse

class TestFunctions(unittest.TestCase):

    def compare_immediate_dominators(self, start, end, edges):
        G = nx.DiGraph(edges)
        idom_nx = sorted(nx.immediate_dominators(G, start).items())

        cfg = ControlFlowGraph.fromEdgeList(start, end, edges)

        dom = dominators(cfg)
        idom_hw = immediateDominator(dom)

        # print(idom_nx)
        # print(idom_hw)

        for node, idom in idom_nx:
            if node == start:
                self.assertEqual(idom_hw[node], '')
            else:
                self.assertEqual(idom_hw[node], idom, "nx: {}, homework: {}".format(idom_nx, idom_hw))

    def compare_dominance_frontiers(self, start, end, edges):
        G = nx.DiGraph(edges)
        dom_frontier_nx = sorted((u, sorted(df)) for u, df in nx.dominance_frontiers(G, start).items())
        cfg = ControlFlowGraph.fromEdgeList(start, end, edges)
        
        control_nodes = findControlNodes(cfg, reverse=True)
        control_dependents = {k:[] for k in cfg.nodes}

        for controller in control_nodes:
            for controllee in control_nodes[controller]:
                if controllee == '':
                    continue
                control_dependents[controllee].append(controller)

        # print(dom_frontier_nx)
        # print(control_dependents)

        for node, frontiers in dom_frontier_nx:
            self.assertListEqual(sorted(control_dependents[node]), sorted(frontiers), "node: {}".format(node))

    def test_immediate_dominators(self):
        graphs = generateGraphList()
        for g in graphs:
            self.compare_immediate_dominators(g['start'], g['end'], g['edges'])

    def test_dominance_frontiers(self):
        graphs = generateGraphList()
        for g in graphs:
            self.compare_dominance_frontiers(g['start'], g['end'], g['edges'])



if __name__ == "__main__":
    unittest.main()