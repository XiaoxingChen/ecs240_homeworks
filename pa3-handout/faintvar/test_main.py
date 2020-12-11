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
        {'in': 'p10.txt','expect': 'expected10.txt'},
        {'in': os.path.join('official', '1.in'),'expect':os.path.join('official', '1.out')},
        {'in': os.path.join('official', '2.in'),'expect':os.path.join('official', '2.out')},
        {'in': os.path.join('official', '3.in'),'expect':os.path.join('official', '3.out')},
        {'in': os.path.join('official', '4.in'),'expect':os.path.join('official', '4.out')},
        {'in': os.path.join('official', '5.in'),'expect':os.path.join('official', '5.out')},
        {'in': os.path.join('official', '6.in'),'expect':os.path.join('official', '6.out')},
        {'in': os.path.join('official', '7.in'),'expect':os.path.join('official', '7.out')},
        {'in': os.path.join('official', '8.in'),'expect':os.path.join('official', '8.out')},
        {'in': os.path.join('official', '9.in'),'expect':os.path.join('official', '9.out')},
        {'in': os.path.join('official', '10.in'),'expect':os.path.join('official', '10.out')}

    ]
    return dataset

class Dirs():
    script_folder = os.path.abspath(os.path.dirname(__file__))
    build_root = os.path.join(script_folder, 'build')
    test_folder = os.path.join(script_folder, 'tests')
    test_folder_q1 = os.path.join(script_folder, '..', 'reachingdef', 'tests')
    test_temp_output = os.path.join(build_root, 'temp_test.txt')

    @staticmethod
    def testFilePath(relative_path, question=2):
        if 1 == question:
            return os.path.join(Dirs.test_folder_q1, relative_path)
        else:
            return os.path.join(Dirs.test_folder, relative_path)

    @staticmethod
    def scriptFolder(question=2):
        if 2 == question:
            return Dirs.script_folder
        else:
            return os.path.join(Dirs.script_folder, '..', 'reachingdef')

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

class TestFaintVarFunctions(unittest.TestCase):
    def test_integration(self):
        dataset = integrationTestDataset()
        if not os.path.exists(Dirs.build_root):
            os.mkdir(Dirs.build_root)

        for q_idx in [1,2]:
            for data in dataset:
                if 'expect' not in data:
                    continue

                shell_cmd = " ".join(["./run.sh", Dirs.testFilePath(data['in'], q_idx), Dirs.test_temp_output])
                os.chdir(Dirs.scriptFolder(q_idx))
                os.system(shell_cmd)

                output = parseExpectedFile(Dirs.test_temp_output)

                if not os.path.isfile(Dirs.testFilePath(data['expect'], q_idx)):
                    continue
                output_expected = parseExpectedFile(Dirs.testFilePath(data['expect'], q_idx))

                # print(output, output_expected)
                self.assertDictEqual(output, output_expected)

    def test_post_order(self):
        problem = parseInputFile(Dirs.testFilePath('p2.txt'))
        self.assertListEqual([9,8,4,6,7,5,3,2,1], postOrder(problem.cfg))



if __name__ == "__main__":
    unittest.main(verbosity=2)