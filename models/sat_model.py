from itertools import product

from networkx import non_edges


def create_encoding_dict(node_pairs):
    encoding_dict = {}
    for i, node_pair in enumerate(node_pairs):
        encoding_dict[i] = node_pair
        encoding_dict[node_pair] = i
    return encoding_dict


def get_clauses(g, starting_node=None, finishing_node=None):
    ranking = range(len(g.nodes))
    node_pairs = product(ranking, g.nodes)
    encoding_dict = create_encoding_dict(node_pairs)

    # 1. Each node j must appear in the path.
    node_must_appear = []
    for j in g.nodes:
        node_must_appear.append([encoding_dict[(i, j)] for i in ranking])
    #node_must_appear = [encoding_dict[node_pair] for node in g.nodes if node in node_pairs]

    # 2. No node j appears twice in the path.
    no_appear_twice = []
    for i in ranking:
        for j in g.nodes:
            for k in ranking:
                if i != k:
                    no_appear_twice.append([-encoding_dict[(i, j)], -encoding_dict[(k, j)]])

    # 3. Every position i on the path must be occupied.
    occupation = []
    for i in ranking:
        occupation.append([encoding_dict[(i, j)] for j in g.nodes])

    # 4. No two nodes j and k occupy the same position in the path.
    no_same_occupation = []
    for i in ranking:
        for j in g.nodes:
            for k in g.nodes:
                if j != k:
                    no_same_occupation.append([-encoding_dict[(i, j)], -encoding_dict[(i, k)]])

    # 5. Nonadjacent nodes i and j cannot be adjacent in the path.
    non_adjacency = []
    for i, j in non_edges(g):
        for k in list(ranking)[:-1]:
            k_1 = k + 1
            non_adjacency.append([-encoding_dict[(k, i)], -encoding_dict[k_1, j]])

    # 6. Starting Node
    starting_clause = []
    if starting_node is not None:
        starting_clause.append(encoding_dict[0, starting_node])

    # 7. Finishing Node
    finishing_clause = []
    if finishing_node is not None:
        finishing_clause.append(encoding_dict[(len(g.nodes) - 1, finishing_node)])

    ret = node_must_appear + no_appear_twice + occupation + no_same_occupation + non_adjacency + starting_clause + finishing_clause
    return ret