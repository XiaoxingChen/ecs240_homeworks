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
        key: node (int) 
        val: layer (int)

    self.successors:
        key: node (int) 
        val: set() (set of nodes)
    """
    def __init__(self):
        self.successors = {}
        self.layer_of_node = {}
        self.nodes_in_layer = {}

    def layer(self, node):
        return self.layer_of_node[node]

    def maxLayer(self):
        return max(self.nodes_in_layer.keys())
    
    def nodes(self, layer):
        return self.nodes_in_layer[layer]

    def addNode(self, node, layer):
        self.layer_of_node[node] = layer
        if layer not in self.nodes_in_layer:
            self.nodes_in_layer[layer] = set()
        self.nodes_in_layer[layer].add(node)

    def addEdge(self, from_node, to_node):
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
        delta_layer = self.layer(from_node) - self.layer(to_node)
        return to_node in self.kGenerationSuccessors(from_node, delta_layer)

    def dualNodeGraph(self, target_layer, cumulate_forbiddens):
        """
        Implementation of section 2.3: G' = (V', E')
        """
        dual_node_graph = LayeredGraph()

        for l in range(self.maxLayer(), target_layer, -1):
            for this_node in combination2(self.nodes(l)):
                for next_node in combination2(self.nodes(l-1)):
                    parallel_edge = (this_node[0], next_node[0], this_node[1], next_node[1])
                    cross_edge = (this_node[0], next_node[1], this_node[1], next_node[0])
                    if parallel_edge in cumulate_forbiddens[l] and cross_edge in cumulate_forbiddens[l]:
                        # both are forbidden pairs
                        continue
                    
                    dual_node_graph.addNode(this_node, l)
                    dual_node_graph.addNode(next_node, l-1)
                    dual_node_graph.addEdge(this_node, next_node)

        return dual_node_graph

    def checkPathVertexDisjoint(self, s1, t1, s2, t2, forbidden_pairs):
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
        
        dual_node_graph = self.dualNodeGraph(target_layer, forbidden_pairs)
        
        for s2_suc in kGenerationSuccessors(successors, s2, delta_layer):
            dual_node_from = sorted([s1, s2_suc])
            dual_node_to = sorted([t1, t2])
            
            if dual_node_graph.checkConnected(dual_node_from, dual_node_to):
                return True
        return False

class ForbiddenPair():
    def __init__(self, max_layer):
        """
        self.forbidden_pairs: 
            key: layer (int)
            val: 4-tuple (from, to, from, to) in set()
        """
        self.forbidden_pairs = {k: set() for k in range(max_layer + 1)}

    def addForbiddenPair(self, layer, from1, to1, from2, to2):
        self.forbidden_pairs[layer].add((from1, to1, from2, to2))
        self.forbidden_pairs[layer].add((from2, to2, from1, to1))

    def cumulate(self, start_layer_inclusive):
        """
        Implemention of figure 4: step 5.
        (const member function)
        """
        ret = set()
        for i in range(start_layer_inclusive, self.maxLayer() + 1):
            ret.update(self.forbidden_pairs[i])
        return ret


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
        if its_type not in self.nodes_in_type:
            self.nodes_in_type[its_type] = []

        self.nodes_in_type[its_type].append(var)

    def addStatement(self, tuple_len_4):
        self.raw_statements.append(tuple_len_4)

    def solve(self):
        realizable_graph = LayeredGraph()
        forbidden_pair = ForbiddenPair()
        for l in range(self.maxLayer(), 0, -1):
            # 1. 2. 3.
            v_ccp = list(realizable_graph.nodes(l)) 
            c_ccp = list(realizable_graph.nodes(l-1))
            s_ccp = []
            # 4. 
            for d, p, _, z in self.directAssignments(l):
                for q in realizable_graph.nodes(l):
                    if realizable_graph.checkConnected(p, q):
                        s_ccp.append((q,z))
            # 5.
            forbiddens = forbidden_pair.cumulate(l+1)
            # 6.
            for d1, p1, d2, p2 in self.copyingStatements(l):
                for q1, q2 in combination2(realizable_graph.nodes(l)):
                    if realizable_graph.checkPathVertexDisjoint(p1, q1, p2, q2, forbiddens):
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
            self.forbidden_pairs[l] = set()
            # 11. update forbidden_pair of this layer
            for pair in combination2(lamda1_ccp):
                if pair not in lamda2_ccp:
                    self.forbidden_pairs[l].add(pair)
    

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