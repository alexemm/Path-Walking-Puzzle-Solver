# From: https://stackoverflow.com/questions/47982604/hamiltonian-path-using-python

def hamilton2(graph, start_v):
    size = len(graph)
    # if None we are -unvisiting- coming back and pop v
    to_visit = [None, start_v]
    path = []
    visited = set([])
    while to_visit:
        v = to_visit.pop()
        if v:
            path.append(v)
            if len(path) == size:
                break
            visited.add(v)
            for x in graph[v] - visited:
                to_visit.append(None)  # out
                to_visit.append(x)  # in
        else:  # if None we are coming back and pop v
            visited.remove(path.pop())
    return path


def hamilton(G, size, pt, path=[]):
    print('hamilton called with pt={}, path={}'.format(pt, path))
    if pt not in set(path):
        path.append(pt)
        if len(path)==size:
            return path
        for pt_next in G.get(pt, []):
            res_path = [i for i in path]
            candidate = hamilton(G, size, pt_next, res_path)
            if candidate is not None:  # skip loop or dead end
                return candidate
        print('path {} is a dead end'.format(path))
    else:
        print('pt {} already in path {}'.format(pt, path))
    # loop or dead end, None is implicitly returned