import os
import sys
import unittest
import shutil
from main import *

def integrationTestDataset():
    dataset = [
        {'in': 'p1.txt','expect': 'expected1.txt'},
        {'in': 'p2.txt','expect': 'expected2.txt'},
        {'in': 'p3.txt','expect': 'expected3.txt'}
    ]
    return dataset

class Dirs():
    script_folder = os.path.abspath(os.path.dirname(__file__))
    build_root = os.path.join(script_folder, 'build')
    test_folder = os.path.join(script_folder, 'tests')
    test_temp_output = os.path.join(build_root, 'temp_test.txt')

    @staticmethod
    def testFilePath(relative_path):
        return os.path.join(Dirs.test_folder, relative_path)

def parseFaintVariables(filename):
    """
    return dict, key: int, val: tuple
    """
    faints = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] != 'fvin':
                raise RuntimeError()
            faints[int(line_content[1])] = tuple(sorted([int(v) for v in line_content[2:3]]))

    return faints

def randomControlFlowGraphGenerator(node_num, entry_node, exit_node):
    assert(entry_node != exit_node)
    import random
    cfg = ControlFlowGraph(node_num, entry_node, exit_node)
    src_list, dst_list = [entry_node], [exit_node]
    internal_nodes = set([i for i in range(node_num - 2)])

    max_val = node_num
    if entry_node >= max_val:
        max_val -= 1
    if exit_node >= max_val:
        max_val -= 1

    internal_nodes = set([i for i in range(max_val)])
    internal_nodes.discard(entry_node)
    internal_nodes.discard(exit_node)

    seq = list(internal_nodes)
    for n in seq:
        dst = random.choice(dst_list)
        cfg.addEdge(n, dst)
        dst_list.append(n)

    random.shuffle(seq)
    for n in seq:
        src = random.choice(src_list)
        cfg.addEdge(src, n)
        src_list.append(n)

    return cfg



class TestFaintVarFunctions(unittest.TestCase):
    def test_integration(self):
        dataset = integrationTestDataset()
        if not os.path.exists(Dirs.build_root):
            os.mkdir(Dirs.build_root)

        for data in dataset:
            if 'expect' not in data:
                continue
            problem = parseInputFile(Dirs.testFilePath(data['in']))
            blocks = problem.solve()
            writeOutput(Dirs.test_temp_output, blocks.fvin)

            output = parseFaintVariables(Dirs.test_temp_output)
            output_expected = parseFaintVariables(Dirs.testFilePath(data['expect']))

            self.assertDictEqual(output, output_expected)

    def test_post_order(self):
        problem = parseInputFile(Dirs.testFilePath('p2.txt'))
        self.assertListEqual([9,8,4,6,7,5,3,2,1], postOrder(problem.cfg))

    def test_cfg_random_generator(self):
        cfg = randomControlFlowGraphGenerator(5, 0, 5)
        print(cfg.successors)


if __name__ == "__main__":
    unittest.main(verbosity=2)