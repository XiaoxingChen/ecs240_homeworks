import os
import sys
import unittest
from main import *

test_suites = [
    ["p1.txt", "expected1.txt"],
    ["p2.txt", "expected2.txt"],
    ["p3.txt", "expected3.txt"],
    # ["p4.txt", "expected4.txt"],
    ["p5.txt", "expected5.txt"],
    ["p6.txt", "expected6.txt"],
    ["p7.txt", "expected7.txt"],
]

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

if __name__ == "__main__":
    unittest.main()
