import os
import sys
class ControlFlowGraph:
    """
    copy from pa1-handout/main.py
    """
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

class BlockHub():
    def __init__(self, num_var, num_block):
        self.all_blocks = [i for i in range(1, num_block + 1)]
        self.all_vars = set([i for i in range(1, num_var + 1)])
        self.lhs = {i: set() for i in self.all_blocks}
        self.rhs = {i: set() for i in self.all_blocks}
        self.fvin = {i: self.all_vars for i in self.all_blocks}
        self.rdout = {i: set() for i in self.all_blocks}

    def addBlock(self, idx, lhs=set(), rhs=set()):
        self.lhs[idx] = lhs
        self.rhs[idx] = rhs

def isPrint(var):
    return var == 0

class Problem():
    def __init__(self, v_b_e_s_x):
        """
        The problem declaration line “p V B E s x” declares that there are V variables, B basic
        blocks, and E edges in the CFG. Variables are labeled from 1 to V , and basic blocks
        are labeled from 1 to B. s, x ∈ [1, B] are entry and exit.

        input: v_b_e_s_x
            type: int in list
        """
        num_var, num_block, num_edge, entry_block, exit_block = v_b_e_s_x
        self.num_var = num_var
        self.num_block = num_block
        self.num_edge = num_edge
        self.entry_block = entry_block
        self.exit_block = exit_block

        self.cfg = ControlFlowGraph(self.num_block, self.entry_block, self.exit_block)
        self.blocks = BlockHub(num_var, num_block)
        self.all_vars = set([i for i in range(1, num_var + 1)])


    def addEdge(self, from_idx, to_idx):
        self.cfg.addEdge(from_idx, to_idx)

    def addBlock(self, i_l_ri_rn):
        self.blocks.addBlock(i_l_ri_rn[0], set(i_l_ri_rn[1:2]), set(i_l_ri_rn[2:]))

    def updateReachingDefinition(self):
        order = postOrder(self.cfg)[::-1]
        updated = False
        for idx in order:
            rdin = set()
            for pred in self.cfg.predecessors[idx]:
                rdin.update(self.blocks.rdout[pred])

            if len(self.blocks.lhs[idx]) == 0 or isPrint(list(self.blocks.lhs[idx])[0]):
                self.blocks.rdout[idx] = rdin
                # print("i: {}, rdout: {}".format(idx, rdin))
                continue

            lhs = list(self.blocks.lhs[idx])[0]
            gen_set = set()
            kill_set = set()

            # kill_set
            for block_idx in rdin:
                if lhs in self.blocks.lhs[block_idx]:
                    kill_set.add(block_idx)

            # gen_set
            gen_set.add(idx)

            new_rdout = rdin.difference(kill_set).union(gen_set)
            # print("i: {}, rdin: {}, kill: {}, gen: {}, rdout: {}".format(idx, rdin, kill_set, gen_set, new_rdout))
            if new_rdout != self.blocks.rdout[idx]:
                updated = True
                self.blocks.rdout[idx] = new_rdout

        return updated

    def updateFaintVariable(self):
        order = postOrder(self.cfg)
        updated = False
        # print(order)
        for idx in order:
            fvout = set(self.all_vars)
            for succ in self.cfg.successors[idx]:
                fvout.intersection_update(self.blocks.fvin[succ])

            if len(self.blocks.lhs[idx]) == 0:
                self.blocks.fvin[idx] = fvout
                continue

            lhs = list(self.blocks.lhs[idx])[0]
            gen_set = set()
            kill_set = set()

            # ConstGen 1. n is assignment x = e, x \not \in Opd (e)
            if lhs not in self.blocks.rhs[idx] and not isPrint(lhs):
                gen_set.add(lhs)

            # ConstKill 1. n is use(x)
            if isPrint(lhs):
                kill_set.update(self.blocks.rhs[idx])

            # DepKill 1. Opd(e) \cap Var n is assignment x = e, x \not in X
            if lhs not in fvout:
                kill_set.update(self.blocks.rhs[idx])

            # print("i: {}, out: {}, kill: {}, gen: {}".format(idx, fvout, kill_set, gen_set))

            new_fvin = fvout.difference(kill_set).union(gen_set)
            if new_fvin != self.blocks.fvin[idx]:
                updated = True
                self.blocks.fvin[idx] = new_fvin

        return updated


    def solve(self, question=2):
        fix_point = False
        for i in range(20):
            if 1 == question:
                update = self.updateReachingDefinition()
            else:
                update = self.updateFaintVariable()
            if not update:
                fix_point = True
                break
        if not fix_point:
            print("failed!")
        return self.blocks

def postOrder(cfg, root=None, visited=None):
    """
    recursive version
    """
    seq = []

    root = cfg.entry_node if root is None else root
    visited = set() if visited is None else visited
    for node in cfg.successors[root]:
        if node in visited:
            continue
        visited.add(node)
        seq += postOrder(cfg, node, visited)

    seq.append(root)
    return seq


def parseInputFile(filename):
    problem = None
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'c':
                continue

            line_content[1:] = [int(v) for v in line_content[1:]]
            if line_content[0] == 'p':
                problem = Problem(line_content[1:])
            elif line_content[0] == 'b':
                problem.addBlock(line_content[1:])
            elif line_content[0] == 'e':
                problem.addEdge(line_content[1], line_content[2])
            else:
                pass

    return problem

def writeOutput(filename, block_hub, question=2):
    output_str = ''
    for k in block_hub.all_blocks:
        if 1 == question:
            output_str += ' '.join(['rdout', str(k)] + [str(v) for v in sorted(block_hub.rdout[k])]) + '\n'
        else:
            output_str += ' '.join(['fvin', str(k)] + [str(v) for v in sorted(block_hub.fvin[k])]) + '\n'

    with open(filename, 'w') as f:
        f.write(output_str)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("please specify input and output!")
        quit()

    input_filename, output_filename = [os.path.join(os.path.realpath(p)) for p in sys.argv[1:3]]
    problem = parseInputFile(input_filename)
    blocks = problem.solve(question=2)
    writeOutput(output_filename, blocks, question=2)