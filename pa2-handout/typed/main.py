import os
import sys

class TypedPointToAnalysis():
    def __init__(self, n, s):
        self.variable_num = n
        self.statement_num = s
        self.type_dict = {}
        self.raw_statements = []

    def addType(self, var, its_type):
        # be careful that "type" is a keyword of python
        self.type_dict[var] = its_type

    def addStatement(self, tuple_len_4):
        self.raw_statements.append(tuple_len_4)
    

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