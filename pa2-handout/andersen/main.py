import sys
import os

class SetOfStatements:
    def __init__(self, node_num, stat_num):
        self.node_num = node_num
        self.stat_num = stat_num
        self.pairs = {}
        self.statements = []

    def addPair(self, from_node, to_node):
        if from_node not in self.pairs.keys():
            self.pairs[from_node] = set(to_node)
        else:
            self.pairs[from_node].add(to_node)

    def addStatements(self, lst):
        self.statements.append(lst)

    def __str__(self):
        output = "node_num: {}\n".format(self.node_num) + "stat_num: {}\n".format(self.stat_num)
        output += "pairs: {}\n".format(self.pairs) + "statements: {}".format(self.statements)
        return output

    def rewriteStatements(self):
        for statement in self.statements:
            if statement[0] == 0 and statement[2] == -1:
                self.addPair(statement[1], statement[3])
            else:
                pass
    
    def getPairs(self):
        return self.pairs
    
    def removeUnnecessaryNodes(self):
        pass

def parseInput(input_file):
    sos = None
    with open(input_file, "r") as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'p':
                sos = SetOfStatements(line_content[1], line_content[2])
            elif line_content[0] == 's':
                sos.addStatements(line_content[1:5])
            else:
                pass
    return sos

# output in random order
def writeToOutput(pairs, output_file):
    output = ""
    for from_node in pairs:
        for to_node in pairs[from_node]:
            output += ' '.join(['pt', from_node, to_node]) + '\n'
        
    with open(output_file, 'w+') as f:
        f.write(output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("The number of arguments is wrong, please try again")
    input_file, output_file = [os.path.abspath(os.path.realpath(n)) for n in sys.argv[1:3]]
    sos = parseInput(input_file)
    
    # pairs= {"1": {"1", "2",}}
    # writeToOutput(pairs, output_file)