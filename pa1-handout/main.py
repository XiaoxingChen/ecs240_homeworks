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
    # """
    # """
    if not reverse:
        root = cfg.entry_node
        successors = cfg.successors
        predecessors = cfg.predecessors
    else:
        root = cfg.exit_node
        successors = cfg.predecessors
        predecessors = cfg.successors

    print("[WARNING]: [todo] BFS once cannot ensure the convergence of dominator calculation!")

    # BFS 
    dom = {k: set(cfg.nodes) for k in cfg.nodes}
    fifo = [root]
    not_visited = set(cfg.nodes)
    while len(fifo) > 0:
        node = fifo[0]
        if node not in not_visited:
            fifo.pop(0)
            continue
        # print(node)
        intersect = set(cfg.nodes) if node != root else set()
        for predecessor in predecessors[node]:
            intersect.intersection_update(dom[predecessor])
    
        dom[node] = intersect.union(set([node]))
        not_visited.remove(node)
        fifo.pop(0)
        fifo += list(successors[node])
        
    return dom

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
    idom = immediateDominator(dom)
    cd = findControlNodes(cfg)
    outputToFile(output_filename, idom, cd)
    
    
