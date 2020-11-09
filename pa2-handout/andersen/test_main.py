import os
import sys
import unittest
import random
from main import *
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
from pointer_hub import PointerHub

test_suites = [
    ["p1.txt", "expected1.txt"],
    ["p2.txt", "expected2.txt"],
    ["p3.txt", "expected3.txt"],
    # ["p4.txt", "expected4.txt"],
    ["p5.txt", "expected5.txt"],
    ["p6.txt", "expected6.txt"],
    ["p7.txt", "expected7.txt"],
]

no_expected_suites = ['p9.txt', 'p10.txt', 'p11.txt']

def runAndersen(filename):
    sos = parseInput(filename)
    sos.rewriteStatements()
    sos.andersenAlgorithm()
    realizable_pairs = sos.removeUnnecessaryNodes()
    return realizable_pairs

def parseExpectedOutput(filename):
    pairs = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[1] not in pairs:
                pairs[line_content[1]] = set()
            pairs[line_content[1]].add(line_content[2])
    return pairs

class andersenTest(unittest.TestCase):
    def test_overall(self):
        script_folder = os.path.abspath(os.path.dirname(__file__))
        test_folder = os.path.join(script_folder, "tests")
        for input_file, expected in test_suites:
            get_pairs = runAndersen(os.path.join(test_folder, input_file))
            expected_pairs = parseExpectedOutput(os.path.join(test_folder, expected))
            self.assertDictEqual(get_pairs, expected_pairs)

    def test_monte_carlo(self):
        script_folder = os.path.abspath(os.path.dirname(__file__))
        test_folder = os.path.join(script_folder, "tests")
        for filename in no_expected_suites[:]:
            input_filename = os.path.join(test_folder, filename)
            get_pairs = runAndersen(input_filename)
            sos = parseInput(input_filename)
            pointer_hub = PointerHub([i + 1 for i in range(sos.node_num)])
            
            sampled_pairs = set()
            calculated_pairs = set()
            for from_node in get_pairs:
                for to_node in get_pairs[from_node]:
                    calculated_pairs.add((int(from_node), int(to_node)))

            for _ in range(5000):
                idx = int(len(sos.statements) * random.random())
                s = [int(v) for v in sos.statements[idx]]
                pair = pointer_hub.update(s)
                if pair is None:
                    continue
                sampled_pairs.add(pair)
                self.assertIn(pair, calculated_pairs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
