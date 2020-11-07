import os
import sys

def combination2(nodes):
    ret = []
    sorted_nodes = sorted(nodes)
    for i in range(len(sorted_nodes)):
        for j in range(0, i):
            ret.append((sorted_nodes[j], sorted_nodes[i]))
    return ret

class LayeredGraph():
    """
    self.nodes_in_layer:
        key: layer (int) 
        val: set of nodes

    self.layer_of_node:
        key: node (int or 2-tuple) 
        val: layer (int)

    self.successors:
        key: node (int or 2-tuple) 
        val: set() (set of nodes)
    """
    def __init__(self):
        self.successors = {}
        self.layer_of_node = {}
        self.nodes_in_layer = {}

    def layer(self, node):
        if hasattr(node, '__getitem__'):
            node = tuple(sorted(node))
        return self.layer_of_node[node]

    def maxLayer(self):
        return max(self.nodes_in_layer.keys())
    
    def nodes(self, layer):
        return self.nodes_in_layer[layer]

    def addNode(self, node, layer):
        if hasattr(node, '__getitem__'):
            node = tuple(sorted(node))

        self.layer_of_node[node] = layer

        if layer not in self.nodes_in_layer:
            self.nodes_in_layer[layer] = set()
        self.nodes_in_layer[layer].add(node)

        if node not in self.successors and layer != 0:
            self.successors[node] = set()

    def addEdge(self, from_node, to_node):
        if hasattr(from_node, '__getitem__'):
            from_node = tuple(sorted(from_node))
        if hasattr(to_node, '__getitem__'):
            to_node = tuple(sorted(to_node))

        if from_node not in self.layer_of_node:
            print("node {} not found".format(from_node))
        
        if to_node not in self.layer_of_node:
            print("node {} not found".format(to_node))

        if from_node not in self.successors:
            self.successors[from_node] = set()
        self.successors[from_node].add(to_node)

    def kGenerationSuccessors(self, node, k):
        """
        Return the k-th generation successors of a layered graph.
        The layred graph is represented in successors_dict.
        """
        if hasattr(node, '__getitem__'):
            node = tuple(sorted(node))
        fifo = set([node])
        for i in range(k):
            nodes_this_layer = list(fifo)
            fifo = set()
            for node in nodes_this_layer:
                fifo.update(self.successors[node])

        return fifo

    def checkConnected(self, from_node, to_node):
        """
        Check path exist in a layered graph from `from_node` to `to_node`.
        The layred graph is represented in successors_dict.
        """
        if hasattr(from_node, '__getitem__'):
            from_node = tuple(sorted(from_node))
        if hasattr(to_node, '__getitem__'):
            to_node = tuple(sorted(to_node))
        delta_layer = self.layer(from_node) - self.layer(to_node)
        return to_node in self.kGenerationSuccessors(from_node, delta_layer)

    def dualNodeGraph(self, target_layer, forbidden_pair):
        """
        Implementation of section 2.3: G' = (V', E')
        forbidden_pair:
            object of class ForbiddenPair()
        """
        dual_node_graph = LayeredGraph()

        for l in range(self.maxLayer(), target_layer, -1):
            for this_node in combination2(self.nodes(l)):
                for next_node_0 in self.successors[this_node[0]]:
                    for next_node_1 in self.successors[this_node[1]]:
                        edge_pair = [(this_node[0], next_node_0),(this_node[1], next_node_1)]
                        if forbidden_pair.existsAbove(edge_pair, l):
                            continue
                        next_node = [next_node_0, next_node_1]
                        dual_node_graph.addNode(this_node, l)
                        dual_node_graph.addNode(next_node, l-1)
                        dual_node_graph.addEdge(this_node, next_node)

        return dual_node_graph

    def checkPathVertexDisjoint(self, s1, t1, s2, t2, dual_node_graph):
        """
        Check vertex disjoint path exist in a layered graph.
        path1: start from s1 at layer_s1, target at t1;
        path2: start from s2 at layer_s2, target at t2;

        Implementation of Theorem 6. in Paper 2.3;
        """
        assert(self.layer(t1) == self.layer(t2))
        target_layer = self.layer(t1)

        if self.layer(s1) > self.layer(s2):
            s1, t1, s2, t2 = s2, t2, s1, t1
        
        # dual_node_graph = self.dualNodeGraph(target_layer, forbidden_pair)
        delta_layer = self.layer(s2) - self.layer(s1)
        for s2_suc in self.kGenerationSuccessors(s2, delta_layer):
            dual_node_from = [s1, s2_suc]
            dual_node_to = [t1, t2]
            
            if dual_node_graph.checkConnected(dual_node_from, dual_node_to):
                return True
        return False

class ForbiddenPair():
    def __init__(self, max_layer):
        """
        self.forbidden_pairs: 
            key: layer (int)
            val: 2x2-tuple ((from1, to1), (from2, to2)) in set()
            # to keep the unary of set element, be sure from1 < from2.
        """
        self.max_layer = max_layer
        self.layer_pairs_dict = {k: set() for k in range(max_layer + 1)}

    def clearLayer(self, layer):
        self.layer_pairs_dict[layer] = set()

    def add(self, layer, pair):
        pair = tuple( sorted(pair) )
        self.layer_pairs_dict[layer].add(pair)

    def existsAbove(self, pair, start_layer_exclusive):
        """
        Implemention of figure 4: step 5.
        (const member function)
        return: set() of 2x2-tuple
        """
        assert(type(start_layer_exclusive) == int)

        pair = tuple( sorted(pair) )
        cumulated = set()
        for i in range(start_layer_exclusive, self.max_layer + 1):
            if pair in self.layer_pairs_dict[i]:
                return True
        return False


class ConcurrentCopyPropagation():
    def __init__(self, variables, constants, statements):
        """
        """
        assert(type(variables) == set)
        assert(type(constants) == set)
        self.variables = variables
        self.constants = constants
        self.statements = statements

    def statementsConstToVar(self):
        ret = []
        for s in self.statements:
            if s[0] in self.variables and s[1] in self.constants:
                ret.append(s)
        return ret

    def statementsVarToVar(self):
        ret = []
        for s in self.statements:
            if s[0] in self.variables and s[1] in self.variables:
                ret.append(s)
        return ret

    def findAvailablePairs(self, X, x, Y, y):
        """
        Implementation of Theorem 8, three steps
        """
        lambda_ = set()
        # step 1.
        for Z, z in self.statementsConstToVar():
            if(Z != X):
                lambda_.add(tuple( sorted([(X, x),(Z, z)]) ))
        
        # step 2. 3.
        for Z, P in self.statementsVarToVar():
            if P != X:
                continue
            if Z != X:
                lambda_.add(tuple( sorted([(X, x),(Z, x)]) ))
            if Z != Y:
                lambda_.add(tuple( sorted([(Z, x),(Y, y)]) ))

        return lambda_

    def solve1ccp(self):
        """
        Implementation of THEOREM 7.
        """
        lambda_ = set(self.statementsConstToVar())
        while True:
            new_lambda = set()
            for var_x, const_x in lambda_:
                for var_l, var_r in self.statementsVarToVar():
                    if var_r != var_x:
                        continue
                    new_lambda.add((var_l, const_x))
            
            if new_lambda.issubset(lambda_):
                break

            lambda_.update(new_lambda)

        return lambda_

    def solve2ccp(self):
        """
        Implementation of THEOREM 8.
        """
        lambda_ = set(combination2(self.statementsConstToVar()))
        while True:
            new_lambda = set()
            for (var_x, const_x), (var_y, const_y) in lambda_:
                new_lambda.update(self.findAvailablePairs(var_x, const_x, var_y, const_y))
                new_lambda.update(self.findAvailablePairs(var_y, const_y, var_x, const_x))

            if new_lambda.issubset(lambda_):
                break

            lambda_.update(new_lambda)
        return lambda_



            


class TypedPointToAnalysis():
    def __init__(self, n, s):
        """
        self.raw_statements:
            4-tuple (order, from, order, to) in list()
        """
        self.variable_num = n
        self.statement_num = s

        self.raw_statements = []
        self.type_dict = {}
        

    def directAssignments(self, target_layer):
        """
        return all direct assignment statements(*^d p = &z) in raw_statements
        (const member function)
        """
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

    def copyingStatements(self, target_layer):
        """
        return all copy statements (*^{d_1}p_1 = *^{d_2}p_2) in raw_statements
        (const member function)
        """
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
                
    def addType(self, var, its_type):
        # be careful that "type" is a keyword of python
        self.type_dict[var] = its_type

    def addStatement(self, tuple_len_4):
        self.raw_statements.append(tuple_len_4)

    def solve(self):
        max_layer = max(self.type_dict.values())
        realizable_graph = LayeredGraph()
        forbidden_pair = ForbiddenPair(max_layer)
        for l in range(max_layer, 0, -1):
            # 1. 2. 3.
            v_ccp = [var for var in self.type_dict.keys() if (self.type_dict[var] == l)] 
            c_ccp = [var for var in self.type_dict.keys() if (self.type_dict[var] == (l-1))]
            s_ccp = []
            # 4. 
            for d, p, _, z in self.directAssignments(l):
                for q in realizable_graph.nodes(l):
                    if realizable_graph.checkConnected(p, q):
                        s_ccp.append((q,z))
            # 5.
            # forbiddens = forbidden_pair.cumulate(l+1)
            # 6.
            dual_node_graph = realizable_graph.dualNodeGraph(l, forbidden_pair)
            for d1, p1, d2, p2 in self.copyingStatements(l):
                for q1, q2 in combination2(realizable_graph.nodes(l)):
                    if realizable_graph.checkPathVertexDisjoint(p1, q1, p2, q2, dual_node_graph):
                        s_ccp.append((q1, q2))
            # 7. update lamda1_ccp
            ccp_problem = ConcurrentCopyPropagation(v_ccp, c_ccp, s_ccp)
            lamda1_ccp = ccp_problem.solve1ccp()
            # 8. update realizable_graph
            for from_node, to_node in lamda1_ccp:
                # [todo] when to call addNode() ?
                realizable_graph.addEdge(from_node, to_node)
            # 9. update lamda2_ccp
            lamda2_ccp = ccp_problem.solve2ccp()
            # 10. initialize forbidden_pair of this layer
            forbidden_pair.clearLayer(l)
            # 11. update forbidden_pair of this layer
            for pair in combination2(lamda1_ccp):
                if pair not in lamda2_ccp:
                    forbidden_pair.add(pair)

        print(realizable_graph.successors)
    

def parseInputFile(filename):
    problem = None
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            line_content[1:] = [int(v) for v in line_content[1:]]
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
    # problem.solve()