import os
import sys

class TypedPointToAnalysis():
    def __init__(self, n, s):
        """
        self.nodes_in_type:
            key: type (int) 
            val: list of nodes

        self.forbidden_pairs: 
            key: layer (int)
            val: 4-tuple (from, to, from, to) in set()

        self.raw_statements:
            4-tuple (order, from, order, to) in list()
        """
        self.variable_num = n
        self.statement_num = s

        self.type_dict = {}
        self.nodes_in_type = {}

        self.raw_statements = []
        self.successors = {}
        self.forbidden_pairs = {}

    def directAssignments(self, target_layer):
        ret = []
        for d, p, to_order, z in self.raw_statements:
            if to_order != -1:
                continue
            if self.type_dict[z] != target_layer - 1:
                continue
            if self.type_dict[p] != target_layer + d:
                continue
            ret.append((d, p, to_order, z))
        return ret

    self.copyingStatements(self, target_layer):
        ret = []
        for d1, p1, d2, p2 in self.raw_statements:
            if d2 < 0:
                continue
            if self.type_dict[p1] != target_layer + d1:
                continue
            if self.type_dict[p2] != target_layer + d2:
                continue
            ret.append((d1, p1, d2, p2))
        return ret

    def cumulateForbiddens(self, start_layer_inclusive):
        ret = set()
        for i in range(start_layer_inclusive, self.maxLayer() + 1):
            ret.update(self.forbidden_pairs[i])
        return ret

                
    def addType(self, var, its_type):
        # be careful that "type" is a keyword of python
        self.type_dict[var] = its_type
        if its_type not in self.nodes_in_type:
            self.nodes_in_type[its_type] = []

        self.nodes_in_type[its_type].append(var)

    def maxLayer(self):
        return max(self.nodes_in_type.keys())

    def addStatement(self, tuple_len_4):
        self.raw_statements.append(tuple_len_4)

    def kGenerationSuccessors(self, node, k):
        fifo = set([node])
        for i in range(k):
            nodes_this_layer = list(fifo)
            fifo = set()
            for node in nodes_this_layer:
                fifo.update(self.successors[node])

        return fifo

    def solve(self):
        for l in range(self.maxLayer(), 0, -1):
            # 1. 2. 3.
            v_ccp = list(self.nodes_in_type[l])
            c_ccp = list(self.nodes_in_type[l-1])
            s_ccp = []
            # 4. 
            for d, p, _, z in self.directAssignments(l):
                for q in self.nodes_in_type(l):
                    if q not in self.kGenerationSuccessors(p, d):
                        continue
                    s_ccp.append((q,z))
            # 5.
            forbiddens = self.cumulateForbiddens(l + 1)
            # 6.
            for d1, p1, d2, p2 in self.copyingStatements(l):
                pass # todo
            # 7.
            # 8.
            # 9.
            # 10.
            self.forbidden_pairs[l] = set()
            # 11.
                

    

def parseInputFile(filename):
    problem = None
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'p':
                problem = TypedPointToAnalysis(line_content[1], line_content[2])
            elif line_content[0] == 't':
                problem.addType(line_content[1], line_content[2])
            elif line_content[0] == 's':
                problem.addStatement(tuple(line_content[1:5]))
            else:
                pass

    return problem

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("please specify input and output!")
        quit()

    input_filename, output_filename = [os.path.realpath(p) for p in sys.argv[1:3]]
    problem = parseInputFile(input_filename)