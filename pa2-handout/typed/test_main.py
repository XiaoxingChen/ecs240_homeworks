import os
import sys
import unittest
from main import *

def ccpTestData():
    dataset = [
        {
            'v': set([101, 102, 103, 104]),
            'c': set([1,2,3]),
            's': [(101,1), (102,3), (103,2), (104,3), (101, 103), (102, 104)],
            'lambda1': set([(101, 2), (101,1), (102,3), (103,2), (104,3)]),
            'lambda2': set([
                # (101,1)
                ((101, 1), (102, 3)),
                ((101, 1), (103, 2)),
                ((101, 1), (104, 3)),
                # (101,2)
                ((101, 2), (102, 3)),
                ((101, 2), (103, 2)),
                ((101, 2), (104, 3)),
                # (102,3)
                ((102, 3), (103, 2)),
                ((102, 3), (104, 3)),
                # (103,2)
                ((103, 2), (104, 3))
            ])
        },
        {
            'v': set([101, 102, 103, 104, 105]),
            'c': set([1,2,3,4]),
            's': [(101,1), (102,2), (103,1), (104,4), (105, 4), (102, 103), (101, 105), (104, 102)],
            'lambda1': set([(101,1), (102,2), (103,1), (104,4), (105, 4), (104, 2), (104, 1), (102, 1), (101,4)])
        },
        {
            'v': set([101, 102]),
            'c': set([1,2]),
            's': [(101, 1), (102, 2), (101, 102), (102, 101)],
            'lambda2': set([
                ((101, 1), (102, 2)),
                ((101, 2), (102, 2)),
                ((101, 1), (102, 1)) ])
        }
    ]
    return dataset

def layeredGraphTestData():
    dataset = [{
        'node_layer': 
            [(301, 3), (302, 3), (303, 3), (304, 3),
             (201, 2), (202, 2), (203, 2), (204, 2),
             (101, 1), (102, 1), (103, 1), (104, 1),
             (  1, 0), (  2, 0), (  3, 0), (  4, 0)],
        'edge': [
            (301, 202), (302, 203), 
            (203, 104), (202, 102), 
            (104,   2), (102,   4)],
        'kGenerationSuccessors':[
            # node, k, expected
            (301, 1, set([202])),
            (301, 2, set([102])),
            (301, 3, set([  4])),
            (302, 1, set([203])),
            (302, 2, set([104])),
            (302, 3, set([  2]))],
        'checkConnected':[
            (301, 4, True),
            (301, 1, False),
            (302, 2, True),
            (302, 4, False)]
    }]
    return dataset

class TestFunctions(unittest.TestCase):
    def test_basic(self):
        print("try test")

    def test_lambda1_ccp(self):
        for data in ccpTestData()[0:2]:
            ccp_problem = ConcurrentCopyPropagation(data['v'], data['c'], data['s'])
            solution = ccp_problem.solve1ccp()
            self.assertSetEqual(solution, data['lambda1'])

    def test_lambda2_ccp(self):
        for data in ccpTestData()[0:2]:
            ccp_problem = ConcurrentCopyPropagation(data['v'], data['c'], data['s'])
            solution = ccp_problem.solve2ccp()
            if 'lambda2' not in data:
                continue
            self.assertSetEqual(solution, data['lambda2'])

    def test_layered_graph(self):
        for data in layeredGraphTestData():
            g = LayeredGraph()
            for node, layer in data['node_layer']:
                g.addNode(node, layer)
            for edge in data['edge']:
                g.addEdge(edge[0], edge[1])

            if 'kGkGenerationSuccessors' in data:
                for node, k, expected in data['kGkGenerationSuccessors']:
                    self.assertSetEqual(g.kGenerationSuccessors(node, k), expected)

            if 'checkConnected' in data:
                for from_, to_, expected in data['checkConnected']:
                    self.assertEqual(g.checkConnected(from_, to_ ), expected, "{} -> {}".format(from_, to_))
                    
                
            


if __name__ == "__main__":
    script_folder = os.path.abspath(os.path.dirname(__file__))
    unittest.main()