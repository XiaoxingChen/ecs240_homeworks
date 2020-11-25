import unittest
import os
import reachingdef.main as m
import reachingdef.exhaustion as e
import random_data_flow

class TestReachingDef(unittest.TestCase):
    def test_reachingDef_result(self):
        # generate random input
        # input file is written to "input.txt"
        random_data_flow.randomDataFlowAnalysisGraph(20, 50, 1, 50)
        
        # reach_def by exhaustion
        e_graph, e_blocks = e.parseInputFile("input.txt")
        e_reach_def = e.reachingDef(e_graph, e_blocks)
        
        # reach_def by main.py
        r= m.Reaching("input.txt", "output.txt")
        r.clean_data()
        r.start()
        m_reach_def = {}
        with open("output.txt", "r") as f:
            for line in f.readlines():
                content = line.split()
                if content[0] == "rdout":
                    if content[1] not in m_reach_def:
                        m_reach_def[content[1]] = set()
                    if len(content) > 2:
                        m_reach_def[content[1]].update(content[2:])
                else:
                    pass
        self.assertDictEqual(e_reach_def, m_reach_def)
        os.remove("input.txt")
        os.remove("output.txt")

if __name__ == "__main__":
    unittest.main()