from faintvar.main import *

def randomControlFlowGraphGenerator(node_num, entry_node, exit_node):
    """
    generate node idx from [1,node_num]
    """
    assert(entry_node != exit_node)
    assert(entry_node <= node_num)
    assert(exit_node <= node_num)
    import random
    cfg = ControlFlowGraph(node_num, entry_node, exit_node)
    src_list, dst_list = [entry_node], [exit_node]

    internal_nodes = set([i for i in range(1, node_num + 1)])
    internal_nodes.discard(entry_node)
    internal_nodes.discard(exit_node)

    seq = list(internal_nodes)
    for n in seq:
        dst = random.choice(dst_list)
        cfg.addEdge(n, dst)
        dst_list.append(n)

    random.shuffle(seq)
    for n in seq:
        src = random.choice(src_list)
        cfg.addEdge(src, n)
        src_list.append(n)

    return cfg

def randomBlockHubGenerator(num_var, num_block):
    """
    variable index from [1,num_var]
    block index from [1,num_var]
    """
    import random
    block_hub = BlockHub(num_var, num_block)

    for idx in block_hub.all_blocks:

        option_list = list(block_hub.all_vars) + [0] * (len(block_hub.all_vars) // 2) + [-1]
        lhs_option = random.choice(option_list)

        if lhs_option < 0:
            block_hub.addBlock(idx)
            continue

        lhs = set([lhs_option])

        # generate RHS.
        var_num = random.choice([0,1,2])
        rhs = set(random.choices(list(block_hub.all_vars), k=var_num))
        block_hub.addBlock(idx, lhs, rhs)

    return block_hub

def randomDataFlowAnalysisGraph(num_var, num_block, start_node, exit_node):
    block_hub = randomBlockHubGenerator(num_var, num_block)
    cfg = randomControlFlowGraphGenerator(num_block, start_node, exit_node)
    edges = [(k, v) for k in cfg.successors.keys() for v in cfg.successors[k]]
    with open("input.txt", "w+") as f:
        # print("p {} {} {} {} {}".format(num_var, num_block, 2 * (num_block - 2), start_node, exit_node))
        f.write("p {} {} {} {} {}\n".format(num_var, num_block, 2 * (num_block - 2), start_node, exit_node))
        for e in edges:
            # print("e {} {}".format(e[0], e[1]))
            f.write("e {} {}\n".format(e[0], e[1]))
        for idx in block_hub.all_blocks:
            param_list = ['b', idx] + list(block_hub.lhs[idx]) + list(block_hub.rhs[idx])
            # print(' '.join([str(p) for p in param_list]))
            f.write(' '.join([str(p) for p in param_list])+'\n')


if __name__ == "__main__":
    randomDataFlowAnalysisGraph(10, 30, 1, 30)
