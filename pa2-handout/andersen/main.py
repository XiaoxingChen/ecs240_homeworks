import sys
import os

class SetOfStatements:
    def __init__(self, node_num, stat_num):
        self.node_num = node_num
        self.stat_num = stat_num
        self.extend_node_num = node_num
        self.extend_stat_num = stat_num
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

    def extendDeref(self, extra_node_num, statement):
        pass

    # treat the statements like a queue
    def rewriteStatements(self):
        for statement in self.statements[:]:
            statement = list(map(int, statement))
            # '&' on the right hand side 
            if statement[2] == -1:
                # no deref on the left hand side 
                if statement[0] == 0:
                    self.addStatements(statement)
                    self.extend_stat_num += 1
                    continue

                extra_node_num = statement[0]
                # [2 p -1 q] => [p p+1 p+1 p+2 p+2 q]
                new_nodes = [str(statement[1])]
                for extra_node in range(self.extend_node_num+1, extra_node_num+self.extend_node_num+1):
                    new_nodes.extend([str(extra_node), str(extra_node)])
                new_nodes.append(str(statement[3]))

                #create new statements
                for i in range(0, extra_node_num):
                    self.addStatements(['1', new_nodes[2*i], '0', new_nodes[2*i+1]])
                for i in range(extra_node_num, extra_node_num + 1):
                    self.addStatements(['0', new_nodes[2*i], '-1', new_nodes[2*i+1]])
                
                self.extend_node_num += extra_node_num
                self.extend_stat_num += extra_node_num + 1

            # '*' on the left hand side and no ref or defer in the right hand side
            elif statement[2] == 0:
                # p = q
                if statement[0] == 0:
                    self.addStatements(statement)
                    self.extend_stat_num += 1
                    continue

                extra_node_num = statement[0] - 1
                # [2 p -1 q] => [p p+1 p+1 p+2 p+2 q]
                new_nodes = [str(statement[1])]
                for extra_node in range(self.extend_node_num+1, extra_node_num+self.extend_node_num+1):
                    new_nodes.extend([str(extra_node), str(extra_node)])
                new_nodes.append(str(statement[3]))

                #create new statements
                for i in range(0, extra_node_num):
                    self.addStatements(['1', new_nodes[2*i], '0', new_nodes[2*i+1]])
                for i in range(extra_node_num, extra_node_num + 1):
                    self.addStatements(['0', new_nodes[2*i], '0', new_nodes[2*i+1]])
                
                self.extend_node_num += extra_node_num
                self.extend_stat_num += extra_node_num + 1
            
            # "*" on both sides 
            else:
                extra_node_num = statement[0] + statement[2] - 1
                # **p = **q => *p = t1, *t1 = t2, t2 = *t3, t3 = *q
                new_nodes = [str(statement[1])]
                for extra_node in range(self.extend_node_num+1, extra_node_num+self.extend_node_num+1):
                    new_nodes.extend([str(extra_node), str(extra_node)])
                new_nodes.append(str(statement[3]))

                #create new statements
                for i in range(0, statement[0]):
                    self.addStatements(['1', new_nodes[2*i], '0', new_nodes[2*i+1]])
                for i in range(statement[0], extra_node_num+1):
                    self.addStatements(['0', new_nodes[2*i], '1', new_nodes[2*i+1]])
                
                self.extend_node_num += extra_node_num
                self.extend_stat_num += extra_node_num + 1
        return self.statements[self.stat_num: self.extend_stat_num]

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
                sos = SetOfStatements(int(line_content[1]), int(line_content[2]))
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
    print(sos.rewriteStatements())
    # writeToOutput(pairs, output_file)