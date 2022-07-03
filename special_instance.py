def create_instance():
    lines = ["S 5 0"]
    for j in range(10):
        lines.append(f"N 0 {j}")
        lines.append(f"N 10 {j}")
    points = [
        (3, 1), (4, 1), (7, 2), (8, 2), (2, 3), (5, 3), (7, 4), (1, 5), (5, 5), (3, 6), (7, 6), (5, 7), (7, 7), (3, 8)
    ]
    points2 = [(i, 0) for i in range(11) if i != 5]
    points3 = [(i, 9) for i in range(11) if i != 5]
    for i, j in points + points2 + points3:
        lines.append(f"N {i} {j}")
    with open("instances/instance1", 'w') as f:
        for line in lines:
            f.write(line + '\n')
    print(lines)