import matplotlib.pyplot as plt
import networkx as nx

from models.dynamic import hamilton2


def read_txt(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    try:
        starting_point = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("S")]
        non_walk_points = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("N")]
        walk_points = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("W")]
        finishing_point = [(int(line.split()[1]), int(line.split()[2])) for line in lines if line.startswith("F")]
    except IndexError:
        print("Lines in file is not structured as (S|W|N|F) x y\n"
              "Please change this and try again!")
        exit(1)
    return starting_point, non_walk_points, walk_points, finishing_point


def check_for_correctness(starting_point, non_walk_points, walk_points, finishing_point):
    try:
        assert len(starting_point) <= 1
        assert len(finishing_point) <= 1
        assert len(non_walk_points) * len(walk_points) == 0 and (len(non_walk_points) > 0 or len(walk_points) > 0)
    except AssertionError:
        print(
            "Either, you have more than one starting point or you use both, walking points and non-walking points in your instance.\n"
            "Please change that and try again!")
        exit(1)


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


def plot_grid(g, ham_path=None, out_path=None):
    edges = []
    if ham_path is not None:
        edges = ham_path_solution_to_edges(ham_path)
    # From: https://stackoverflow.com/questions/35109590/how-to-graph-nodes-on-a-grid-in-networkx
    plt.figure(figsize=(6, 6))
    pos = {(x, y): (y, -x) for x, y in g.nodes()}
    g_edges = g.edges
    colors = ["red" if (i, j) in edges or (j, i) in edges else "black" for (i, j) in g_edges]

    nx.draw(g, pos=pos,
            node_color='lightgreen',
            edge_color=colors,
            # with_labels=True,
            node_size=600)
    if out_path is not None:
        plt.savefig(out_path, format="PNG")
    plt.show()


def setup_graph(starting_point, non_walk_points, walk_points, finishing_point):

    check_for_correctness(starting_point, non_walk_points, walk_points, finishing_point)

    max_x = max(t[0] for t in non_walk_points)
    max_y = max(t[1] for t in non_walk_points)

    g = nx.grid_2d_graph(max_x + 1, max_y + 1)
    g.remove_nodes_from(non_walk_points)
    starting_point = starting_point[0]
    try:
        assert starting_point in g.nodes
        if len(finishing_point) != 0:
            finishing_point = finishing_point[0]
            assert finishing_point in walk_points
    except AssertionError:
        print("Starting/finishing point not in graph!")
        exit(1)
    return g


def get_neighbor_representation(g):
    return {node: set(g.neighbors(node)) for node in g.nodes}


def solve(filename):
    singular_filename = filename.split("/")[-1]
    starting_point, non_walk_points, walk_points, finishing_points = read_txt(filename)
    g = setup_graph(starting_point, non_walk_points, walk_points, finishing_points)
    plot_grid(g, out_path=f"graphs/{singular_filename}.png")
    solution = hamilton2(get_neighbor_representation(g), (5, 0))
    # solution = hamilton(get_neighbor_representation(g), len(g.nodes), (5,0))
    plot_grid(g, solution, out_path=f"solution_graphs/{singular_filename}.png")


if __name__ == '__main__':
    solve("instances/instance1")

