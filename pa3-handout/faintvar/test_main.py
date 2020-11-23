import os
import sys
import unittest
import shutil
from main import *

def integrationTestDataset():
    dataset = [
        {'in': 'p1.txt','expect': 'expected1.txt'},
        {'in': 'p2.txt','expect': 'expected2.txt'},
        {'in': 'p3.txt','expect': 'expected3.txt'},
        {'in': 'p4.txt','expect': 'expected4.txt'},
        {'in': 'p5.txt','expect': 'expected5.txt'}
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
            if line_content[0] == 'c':
                continue
            if line_content[0] != 'fvin':
                raise RuntimeError()
            faints[int(line_content[1])] = tuple(sorted([int(v) for v in line_content[2:]]))

    return faints

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

            # print(output, output_expected)
            self.assertDictEqual(output, output_expected)

    def test_post_order(self):
        problem = parseInputFile(Dirs.testFilePath('p2.txt'))
        self.assertListEqual([9,8,4,6,7,5,3,2,1], postOrder(problem.cfg))



if __name__ == "__main__":
    unittest.main(verbosity=2)