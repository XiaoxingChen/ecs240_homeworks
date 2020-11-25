import unittest
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
        {'in': 'p5.txt','expect': 'expected5.txt'},
        {'in': 'p6.txt','expect': 'expected6.txt'},
        {'in': 'p7.txt','expect': 'expected7.txt'},
        {'in': 'p8.txt','expect': 'expected8.txt'},
        {'in': 'p9.txt','expect': 'expected9.txt'},
        {'in': 'p10.txt','expect': 'expected10.txt'}
    ]
    return dataset

class Dirs():
    script_folder = os.path.abspath(os.path.dirname(__file__))
    build_root = os.path.join(script_folder, 'build')
    test_folder = os.path.join(script_folder, 'tests')
    test_folder_q1 = os.path.join(script_folder, '..', 'reachingdef', 'tests')
    test_temp_output = os.path.join(build_root, 'temp_test.txt')

    @staticmethod
    def testFilePath(relative_path, question=1):
        if 1 == question:
            return os.path.join(Dirs.test_folder_q1, relative_path)
        else:
            return os.path.join(Dirs.test_folder, relative_path)

def parseExpectedFile(filename):
    """
    return dict, key: int, val: tuple
    """
    faints = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'c':
                continue
            if line_content[0] != 'fvin' and line_content[0] != 'rdout':
                raise RuntimeError()
            faints[int(line_content[1])] = tuple(sorted([int(v) for v in line_content[2:]]))

    return faints

class TestReachingDefinitionFunctions(unittest.TestCase):
    def test_integration(self):
        dataset = integrationTestDataset()
        if not os.path.exists(Dirs.build_root):
            os.mkdir(Dirs.build_root)

        for q_idx in [1]:
            for data in dataset:
                if 'expect' not in data:
                    continue
                if not os.path.isfile(Dirs.testFilePath(data['expect'], q_idx)):
                    continue

                r=Reaching(Dirs.testFilePath(data['in']) ,Dirs.test_temp_output)
                r.clean_data()
                r.start()

                output = parseExpectedFile(Dirs.test_temp_output)
                output_expected = parseExpectedFile(Dirs.testFilePath(data['expect'], q_idx))

                self.assertDictEqual(output, output_expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)