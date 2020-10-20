import sys
import copy
import os

class ControlFlowGraph:
    def __init__(self, node_num, entry_node, exit_node):
        self.node_num = node_num
        self.entry_node = entry_node
        self.exit_node = exit_node
        self.successors = {entry_node: set(), exit_node: set()}
        self.predecessors = {entry_node: set(), exit_node: set()}
        self.nodes = set([entry_node, exit_node])

    def addEdge(self, from_node, to_node):
        if from_node not in self.successors:
            self.successors[from_node] = set()
        self.successors[from_node].add(to_node)

        if to_node not in self.predecessors:
            self.predecessors[to_node] = set()
        self.predecessors[to_node].add(from_node)

        self.nodes.add(from_node)
        self.nodes.add(to_node)


def dominators(cfg, reverse=False):
    """Iterative Dominator Algorithm"""
    if not reverse:
        root = cfg.entry_node
        successors = cfg.successors
        predecessors = cfg.predecessors
    else:
        root = cfg.exit_node
        successors = cfg.predecessors
        predecessors = cfg.successors

    dom = {k: set(cfg.nodes) for k in cfg.nodes}
    changed = True
    while(changed):
        changed = False
        for node in cfg.nodes:
            intersect = set(cfg.nodes) if node != root else set()
            for predecessor in predecessors[node]:
                intersect.intersection_update(dom[predecessor])
            new_set = intersect.union(set([node]))
            if new_set != dom[node]:
                changed = True
                dom[node] = new_set

    return dom

def reversePostOrder(cfg):
    """return a list of cfg.nodes in reverse post-order"""
    path, RPO = list(), list()
    visited = set()
    path.append(cfg.entry_node)
    while len(path) > 0:   
        node = path[-1]
        visited.add(node)
        if cfg.successors[node] - visited == set():
            RPO.append(node)
            path.pop()
        else:
            for succ_node in cfg.successors[node]:
                if succ_node not in RPO and succ_node not in path:
                    node = succ_node
                    path.append(node)
                    break
    
    return RPO[::-1]

def immediateDominator(dominators_in):
    idom = {}
    dom = copy.deepcopy(dominators_in)
    fifo = []
    for k in dom:
        if len(dom[k]) == 1:
            fifo.append(k)
            idom = {k: ''} # [for test case]
            break
    
    # BFS
    while len(fifo) > 0:
        dominator = fifo[0]
        for node in dom.keys():
            if dominator not in dom[node]:
                continue
            dom[node].remove(dominator)
            if len(dom[node]) == 1:
                fifo.append(node)
                idom[node] = dominator

        dom.pop(dominator)
        fifo.pop(0)

    return idom


def findControlNodes(cfg, reverse=False):
    # """
    # """
    if not reverse:
        root = cfg.entry_node
        successors = cfg.successors
        predecessors = cfg.predecessors
        post_dom = dominators(cfg, reverse=True)
    else:
        root = cfg.exit_node
        successors = cfg.predecessors
        predecessors = cfg.successors
        post_dom = dominators(cfg, reverse=False)

    # print(post_dom)
    control_nodes = {}
    for node in cfg.nodes:
        # print(node)
        control_nodes[node] = set()
        for successor in successors[node]:
            # 1. Y post-dominates X's successor
            # 2. Y not strictly post-dominates X. 
            set_1 = post_dom[successor]
            set_2 = cfg.nodes.difference(post_dom[node]).union(set([node]))
            control_nodes[node].update(set_1.intersection(set_2))

        if len(control_nodes[node]) == 0: # [for test case]
            control_nodes[node].add('')
        
    return control_nodes
    
def getControlDependence(cfg, idom):
    #reverse the cfg
    root = cfg.exit_node
    successors = cfg.predecessors
    predecessors = cfg.successors

    #get the buttom-up traversal of the dominator tree(reverse-BFS)
    #also record the child of the dominator tree
    #TODO: no idea whether buttom-up traversal is reverse BFS
    traverseOrder = []
    traverseOrder.append(root)
    index = 0
    child = {root: set()}
    while index != len(cfg.nodes):
        cur = traverseOrder[index]
        if cur not in child.keys():
            child[cur] = set()
        for node in cfg.nodes:
            if idom[node] == cur and node not in traverseOrder:
                traverseOrder.append(node)
                child[cur].add(node)
        index += 1
    # traverseOrder = traverseOrder[::-1]

    #reverse dominance frontier(RDF)
    RDF = {}
    for x in traverseOrder[::-1]:
        RDF[x] = set()
        
        #DF-local
        for y in successors[x]:
            if idom[y] != x:
                RDF[x].add(y)

        #DF-up
        for z in child[x]:
            for y in RDF[z]:
                if idom[y] != x:
                    RDF[x].add(y)

    #RDF to CD
    CD = {}
    for x in cfg.nodes:
        CD[x] = set()
    for y in cfg.nodes:
        for x in RDF[y]:
            CD[x].add(y)
    
    return CD

def parseInputFile(filename):
    cfg = None
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'p':
                cfg = ControlFlowGraph(*line_content[1:])
            elif line_content[0] == 'e':
                cfg.addEdge(line_content[1], line_content[2])
            else:
                pass

    return cfg

def outputToFile(filename, idom, cd):
    nodes = sorted(dom.keys())
    output_str = ''
    
    for node in nodes:
        output_str += ' '.join(['idom', node, idom[node]]) + '\n'
    for node in nodes:
        output_str += ' '.join(['cd', node] + sorted(list(cd[node]))) + '\n'

    with open(filename, 'w') as f:
        f.write(output_str)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("please specify input and output!")
        quit()
    
    input_filename, output_filename = [os.path.join(os.path.realpath(p)) for p in sys.argv[1:3]]
    cfg = parseInputFile(input_filename)
    dom = dominators(cfg)
    dom_inverse = dominators(cfg, True)
    idom = immediateDominator(dom)
    idom_inverse = immediateDominator(dom_inverse)
    CD = getControlDependence(cfg, idom_inverse)
    #cd = findControlNodes(cfg)
    outputToFile(output_filename, idom, CD)