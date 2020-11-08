import sys
import os
import copy

class SetOfStatements:
    """Summary of SetofStatements class here.
    Attributes: 
        node_num: An integer count of the nodes from the input.
        stat_num: An integer count of the statements from the input.
        extend_node_num: An integer count of the node after extending the statements with temporary variables.
        extend_stat_num: An integer count of the statements after extending the statements.
        pairs: An dictionary indicating the realizable pairs.
        statements: An list containing the statements.
    """
    def __init__(self, node_num, stat_num):
        self.node_num = node_num
        self.stat_num = stat_num
        self.extend_node_num = node_num
        self.extend_stat_num = stat_num
        self.pairs = {}
        self.statements = []

    def addPair(self, from_node, to_node):
        if from_node not in self.pairs.keys():
            self.pairs[from_node] = set()
            self.pairs[from_node].add(to_node)
        else:
            self.pairs[from_node].add(to_node)

    def addStatements(self, lst):
        self.statements.append(lst)
    
    def setStatement(self, statements):
        """Reset statements after extending statements with temporary variables"""
        self.stat_num = len(statements)
        self.extend_stat_num = len(statements)
        self.statements = statements

    def __str__(self):
        """Just for clear print"""
        output = "node_num: {}\n".format(self.node_num) + "stat_num: {}\n".format(self.stat_num)
        output += "pairs: {}\n".format(self.pairs) + "statements: {}".format(self.statements)
        return output

    # extend the deferences
    def extendDeref(self, extra_node_num, statement, dividing, mark):
        """Extend the dereferences.
        
        Args: 
            extra_node_number: An integer count of temporary variables.
            statement: A list containing the content of the statement.
            dividing: An integer to differentiate left and right dereferences.
            mark: Choose from ("-1", "0", "1") to differentiate 
                the mark ("*", " ", "&") on the right hand side.
        """
        new_nodes = [str(statement[1])]
        for extra_node in range(self.extend_node_num+1, extra_node_num+self.extend_node_num+1):
            new_nodes.extend([str(extra_node), str(extra_node)])
        new_nodes.append(str(statement[3]))

        #create new statements
        self.addStatements(['0', new_nodes[1], '1', new_nodes[0]])
        for i in range(1, dividing):
            self.addStatements(['1', new_nodes[2*i], '0', new_nodes[2*i+1]])
        for i in range(dividing, extra_node_num + 1):
            self.addStatements(['0', new_nodes[2*i], mark, new_nodes[2*i+1]])
        
        self.extend_node_num += extra_node_num
        self.extend_stat_num += extra_node_num + 1

    def rewriteStatements(self):
        """Extend dereferences of the statements and Append those new statements."""
        for statement in self.statements[:]:
            statement = list(map(int, statement))
            # '&' on the right hand side 
            if statement[2] == -1:
                # p = &q
                if statement[0] == 0 or statement[0] >= 1:
                    self.addStatements(list(map(str, statement)))
                    self.extend_stat_num += 1
                    continue
                else:
                    self.extendDeref(statement[0], statement, statement[0], '-1')
            # " " on the right hand side
            elif statement[2] == 0:
                # p = q or *p = q
                if statement[0] == 0 or statement[0] == 1:
                    self.addStatements(list(map(str, statement)))
                    self.extend_stat_num += 1
                    continue
                else:
                    self.extendDeref(statement[0]-1, statement, statement[0], '0')           
            # "*" on the right hand side
            else:
                # p = *q
                if statement[2] == 1 and statement[0] == 0:
                    self.addStatements(list(map(str, statement)))
                    self.extend_stat_num += 1
                    continue
                else:
                    self.extendDeref(statement[0]+statement[2]-1, statement, statement[0], '1')
        # reset the statements
        self.setStatement(self.statements[self.stat_num: self.extend_stat_num])
    
    def removeUnnecessaryNodes(self):
        """Remove temporary nodes
        
        Return: 
            A dict containing the realizable pairs.
        """
        pairs = copy.deepcopy(self.pairs)
        for pair in pairs:
            if int(pair) > self.node_num:
                del self.pairs[pair]
        return self.pairs

    def andersenAlgorithm(self):
        """Andersen's fixpoint algorithm"""
        change = True
        while change:
            change = False
            for statement in self.statements[:]:
                # TODO(Haochen): Test this try-except
                try:
                    if (self.address_of(statement) or self.alias_of(statement) 
                        or self.assign_of(statement) or self.deref_of(statement) or self.derref_of_address(statement)):
                        change = True
                except KeyError:
                    continue

    def address_of(self, statement):
        """Test p = &q
        a = &c => <a, c>
        """
        if statement[0] == '0' and statement[2] == '-1':
            a, c = statement[1], statement[3]
            self.addPair(a, c)
            self.statements.remove(statement)
            return True
        else:
            return False

    def alias_of(self, statement):
        """Test p = q
        b = a, <a, c> => <b, c>
        """
        pairs = copy.deepcopy(self.pairs)
        if statement[0] == '0' and statement[2] == '0':
            b, a = statement[1], statement[3]
            for c in pairs[a]:
                if b not in pairs.keys() or c not in pairs[b]:
                    self.addPair(b, c)
                    return True 
            return False
        else:
            return False

    def assign_of(self, statement):
        """Test p = *q
        d = *a, <a, c>, <c, b> => <d, b>
        """
        pairs = copy.deepcopy(self.pairs)
        if statement[0] == '0' and statement[2] == '1':
            d, a = statement[1], statement[3]
            for c in pairs[a]:
                for b in pairs[c]:
                    if d not in pairs.keys() or b not in pairs[d]:
                        self.addPair(d, b)
                        return True
            return False
        else:
            return False

    def deref_of(self, statement):
        """Test *p = q
        *b = c, <b, a>, <c, b> => <a, b>
        """
        pairs = copy.deepcopy(self.pairs)
        if statement[0] == '1' and statement[2] == '0':
            b, c = statement[1], statement[3]
            for a in pairs[b]:
                for b in pairs[c]:
                    if a not in pairs.keys() or b not in pairs[a]:
                        self.addPair(a, b)
                        return True
            return False
        else:
            return False
    def derref_of_address(self, statement):
        """Test *p = &q
        *b = &c, <b, a> => <a, c>
        """
        """Test **p = &q
        **b = &c, <b, a>, <a, d> => <d, c>
        """
        pairs = copy.deepcopy(self.pairs)
        if statement[0] >= '1' and statement[2] == '-1':
            b, c = statement[1], statement[3]
            if statement[0] == '1':
                for a in pairs[b]:
                    if a not in pairs.keys() or c not in pairs[a]:
                        self.addPair(a, c)
                        return True
                return False
            elif statement[0] == '2':
                for a in pairs[b]:
                    for d in pairs[a]:
                        if d not in pairs.keys() or c not in pairs[d]:
                            self.addPair(d, c)
                            return True
                return False
        else:
            return False

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
    sos.rewriteStatements()
    sos.andersenAlgorithm()
    realizable_pairs = sos.removeUnnecessaryNodes()
    writeToOutput(realizable_pairs, output_file)