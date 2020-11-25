import sys
import networkx as nx

def parseInputFile(filename):
    """Prase Input file into Graph
    
    Args:
        G: int 
            networkx directed graph 
        B: dict (str: list(str))
            blocks information
    """
    G = nx.DiGraph()
    B = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            line_content = line.split()
            if line_content[0] == 'c':
                continue
            if line_content[0] == 'p':
                vertices = [str(v) for v in range(1, int(line_content[2]))]
                G.add_nodes_from(vertices)
            elif line_content[0] == 'b':
                if line_content[1] not in B.keys():
                    B[line_content[1]] = []
                if len(line_content) > 2:
                    B[line_content[1]].extend(line_content[2:])
            elif line_content[0] == 'e':
                G.add_edge(line_content[1], line_content[2])
            else:
                pass
    return G, B

def filterDefNodes(graph, blocks):
    """Get the node only with definition"""
    DefNodes = []
    for node in graph.nodes:
        if len(blocks[node]) > 0 and blocks[node][0] != "0":
            DefNodes.append(node)
    return DefNodes

def reachingDef(graph, blocks):
    """Get reaching definition by exhaustedly iterations

    Args: 
        graph: networkx graph 
            graph of the CFG
        blocks: dict (str: list(str))
            info of the blocks 
    Returns:
        reach_def: dict (str: set(str))
            reaching definition of each OUT[node]
    """
    def_blocks = filterDefNodes(graph, blocks)
    reach_def = {}
    for node in blocks:
        reach_def[node] = set()
    for def_node in def_blocks:
        reach_def[def_node].add(def_node)

    for from_node in def_blocks:
        for to_node in blocks:
            if from_node == to_node:
                continue
            for path in nx.all_simple_paths(graph, from_node, to_node):
                # no such path
                if len(path) == 0:
                    continue
                # connect directly
                if len(path) == 2:
                    if to_node not in def_blocks or blocks[from_node][0] != blocks[to_node][0]:
                        reach_def[to_node].add(from_node)
                    continue               
                # with node inside the path
                reach = True
                for node in path[1:]:
                    if node not in def_blocks:
                        continue
                    if blocks[from_node][0] == blocks[node][0]:
                        reach = False
                        break
                if reach == True:
                    if to_node not in reach_def:
                        reach_def[to_node] = set()
                    reach_def[to_node].add(from_node)
    return reach_def
            
if __name__ == "__main__":
    input = sys.argv[1]
    graph, blocks = parseInputFile(input)
    reach_def = reachingDef(graph, blocks)