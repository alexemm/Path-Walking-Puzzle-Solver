import networkx as nx
import matplotlib.pyplot as plt

from models.dynamic import hamilton


def read_txt(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    starting_point = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("S")]
    non_walk_points = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("N")]
    walk_points = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("W")]

    return starting_point, non_walk_points, walk_points


def check_for_correctness(starting_point, non_walk_points, walk_points):
    assert len(starting_point) <= 1
    assert len(non_walk_points) * len(walk_points) == 0 and (len(non_walk_points) > 0 or len(walk_points) > 0)


def create_grid_graph(walkable_nodes):
    g = nx.Graph()
    g.add_nodes_from(walkable_nodes)
    for i, j in walkable_nodes:
        potential_neighbors = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
        candidates = ((x, y) for x, y in potential_neighbors if (x, y) in walkable_nodes)
        for i_1, j_1 in candidates:
            g.add_edge((i, j), (i_1, j_1))


def ham_path_solution_to_edges(solution):
    edges = []
    for i in range(len(solution) - 1):
        edges.append((solution[i], solution[i + 1]))
    return edges


def plot_grid(g, ham_path=None):
    edges = []
    if ham_path is not None:
        edges = ham_path_solution_to_edges(ham_path)
    # From: https://stackoverflow.com/questions/35109590/how-to-graph-nodes-on-a-grid-in-networkx
    plt.figure(figsize=(6, 6))
    pos = {(x, y): (y, -x) for x, y in g.nodes()}
    g_edges = g.edges
    colors = ["red" if (i, j) in edges or (j, i) in edges else "black" for (i, j) in g_edges]
    print(len([e for e in colors if e == 'red']))
    print(edges)

    nx.draw(g, pos=pos,
            node_color='lightgreen',
            edge_color=colors,
            #with_labels=True,
            node_size=600)
    plt.show()


def setup_graph(filename: str):
    starting_point, non_walk_points, walk_points = read_txt(filename)
    check_for_correctness(starting_point, non_walk_points, walk_points)

    max_x = max(t[0] for t in non_walk_points)
    max_y = max(t[1] for t in non_walk_points)

    g = nx.grid_2d_graph(max_x + 1, max_y + 1)
    g.remove_nodes_from(non_walk_points)

    return g


def get_neighbor_representation(g):
    return {node: list(g.neighbors(node)) for node in g.nodes}


if __name__ == '__main__':
    g = setup_graph("instances/instance1")

    #solution = hamilton(get_neighbor_representation(g), (5, 0))
    solution = hamilton(get_neighbor_representation(g), len(g.nodes), (5,0))
    print(solution)
    plot_grid(g, solution)
