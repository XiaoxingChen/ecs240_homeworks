import os
import sys
import unittest
import shutil
import random
from main import *
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
from pointer_hub import PointerHub


def parseRealizablePair(filename):
    """
    return set of 2-tuple
    """
    point_to = set()
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] != 'pt':
                raise RuntimeError()
            point_to.add(tuple([int(v) for v in line_content[1:3]]))

    return point_to

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
    dataset = [
        {
        'readme': 'this is the graph in paper section 2.2, Figure 3.',
        'node_layer': 
            [(301, 3), (302, 3),
             (201, 2), (202, 2),
             (101, 1), (102, 1),
             (  1, 0), (  2, 0)],
        'edge': [
            (301, 201), (302, 202), 
            (201, 101), (202, 102), 
            (101,   1), (102,   1),
            (301, 202), (302, 201), 
            (101,   2)],
        'kGenerationSuccessors':[
            # node, k, expected
            (301, 1, set([201, 202])),
            (301, 2, set([101, 102])),
            (301, 3, set([  1,   2])),
            (302, 1, set([201, 202])),
            (302, 2, set([101, 102])),
            (302, 3, set([  2]))]
        },
        {
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
            (302, 4, False)],
        'dualNodeGraph':[
            (0, 
            ForbiddenPair(3), 
            {(301, 302): set([(202, 203)]),
            (202, 203): set([(102, 104)]),
            (102, 104): set([(  2,   4)])} )],
        'checkPathVertexDisjoint':
        [
            (301, 4, 302, 2, True),
            (202, 4, 302, 2, True),
            (301, 2, 302, 4, False)
        ]
        
    }]
    return dataset

def integrationTestDataset():
    dataset = [
        {'in': 'p1.txt','expect': 'expected1.txt'},
        {'in': 'p2.txt','expect': 'expected2.txt'},
        {'in': 'p3.txt','expect': 'expected3.txt'},
        {'in': 'p4.txt','expect': 'expected4.txt'},
        {'in': 'p5.txt'},
        {'in': 'p6.txt'},
        {'in': 'p7.txt'},
        {'in': 'p8.txt'},
    ]
    return dataset

class BuildDirectory():
    def __init__(self):
        self.script_folder = os.path.abspath(os.path.dirname(__file__))
        self.build_root = os.path.join(self.script_folder, 'build')
        self.test_folder = os.path.join(self.script_folder, 'tests')
        self.test_temp_output = os.path.join(self.build_root, 'temp_test.txt')

    def testFilePath(self, relative_path):
        return os.path.join(self.test_folder, relative_path)

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

            if 'dualNodeGraph' in data:
                for target_layer, forbiddens, expected_successor_dict in data['dualNodeGraph']:
                    dual_graph = g.dualNodeGraph(target_layer, forbiddens)

                    successor_dict = {}
                    for k in dual_graph.successors:
                        if len(dual_graph.successors[k]) != 0:
                            successor_dict[k] = dual_graph.successors[k]

                    self.assertDictEqual(successor_dict, expected_successor_dict)

            if 'checkPathVertexDisjoint' in data:
                for s1, t1, s2, t2, expected in data['checkPathVertexDisjoint']:
                    dual_node_graph = g.dualNodeGraph(0, ForbiddenPair(g.maxLayer()))
                    result = g.checkPathVertexDisjoint(s1, t1, s2, t2, dual_node_graph)
                    self.assertEqual(result, expected)

    def test_integration(self):
        dataset = integrationTestDataset()
        dirs = BuildDirectory()
        if not os.path.exists(dirs.build_root):
            os.mkdir(dirs.build_root)

        for data in dataset:
            if 'expect' not in data:
                continue
            problem = parseInputFile(dirs.testFilePath(data['in']))
            realizable_graph = problem.solve()
            writeOutput(dirs.test_temp_output, realizable_graph)

            pairs = parseRealizablePair(dirs.test_temp_output)
            pairs_expected = parseRealizablePair(dirs.testFilePath(data['expect']))

            self.assertSetEqual(pairs, pairs_expected)

    def test_monte_carlo(self):
        dataset = integrationTestDataset()
        dirs = BuildDirectory()
        for data in dataset:
            if 'expect' in data:
                continue

            problem = parseInputFile(dirs.testFilePath(data['in']))
            realizable_graph = problem.solve()
            writeOutput(dirs.test_temp_output, realizable_graph)
            calculated_pairs = parseRealizablePair(dirs.test_temp_output)

            pointer_hub = PointerHub(problem.type_dict.keys())

            raw_statements = list(problem.raw_statements)

            sampled_pairs = set()
            for _ in range(50000):
                idx = int(len(raw_statements) * random.random())
                pair = pointer_hub.update(raw_statements[idx])
                if pair is None:
                    continue
                sampled_pairs.add(pair)
                self.assertIn(pair, calculated_pairs)

            # self.assertSetEqual(calculated_pairs, sampled_pairs)

                    

if __name__ == "__main__":
    unittest.main(verbosity=2)