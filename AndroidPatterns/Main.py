#! /usr/bin/env python

from __future__ import division

from collections import Counter
from decimal import Decimal
from itertools import combinations
from math import ceil, sqrt


# get_points and gen_points_dic to calculate ps
def get_points(point1, point2):
    res_points = set()

    if point1[0] == point2[0]:
        if point1[1] < point2[1]:
            return set([(point1[0], y_cord) for y_cord in range(point1[1] + 1, point2[1])])
        else:
            return set([(point1[0], y_cord) for y_cord in range(point2[1] + 1, point1[1])])
    if point1[1] == point2[1]:
        if point1[0] < point2[0]:
            return set([(x_cord, point1[1]) for x_cord in range(point1[0] + 1, point2[0])])
        else:
            return set([(x_cord, point1[1]) for x_cord in range(point2[0] + 1, point1[0])])

    xs = []
    ys = []
    if point1[0] < point2[0]:
        xs = range(point1[0] + 1, point2[0])
    else:
        xs = range(point2[0] + 1, point1[0])
    if point1[1] < point2[1]:
        ys = range(point1[1] + 1, point2[1])
    else:
        ys = range(point2[1] + 1, point1[1])

    for point in [(x_cord, y_cord) for x_cord in xs for y_cord in ys]:
        if point[1] - point1[1] == (point[0] - point1[0]) * ((point2[1] - point1[1]) / (point2[0] - point1[0])):
            res_points.add(point)

    return res_points


def graph_gen(in_points):
    vertices = []
    order_two = combinations(in_points, 2)

    for point1, point2 in order_two:
        middles = get_points(point1, point2)
        if middles == set():
            vertices.append((point1, point2))

    graph = {}
    for vertice in vertices:
        if vertice[0] in graph:
            graph[vertice[0]] += 1
        else:
            graph[vertice[0]] = 1
        if vertice[1] in graph:
            graph[vertice[1]] += 1
        else:
            graph[vertice[1]] = 1

    min_val = min(graph.itervalues())
    max_val = max(graph.itervalues())

    min_points = []
    for point, value in graph.iteritems():
        if value == min_val:
            min_points.append(point)
    min_grads = []
    for i in in_points:
        if i == min_points[0]:
            continue
        if i[0] == min_points[0][0]:
            grad = float("inf")
        else:
            grad = (i[1] - min_points[0][1]) / (i[0] - min_points[0][0])
        min_grads.append(grad)
    sorted_grad = [y_cord for x_cord, y_cord in Counter(min_grads).most_common()]

    init = 1
    ps_min = []
    for i in sorted_grad:
        ps_min = ps_min + [init] * i
        init += 1
    ps_min.reverse()

    min_decreased = range(min_val, 0, -1)
    min_decreased = min_decreased + [1] * (len(in_points) - len(min_decreased) - 1)
    ps_min = [max(x_cord) for x_cord in zip(ps_min, min_decreased)]

    max_increased = range(max_val, 0, -1)
    max_increased = [max_val] * (len(in_points) - len(max_increased) - 1) + max_increased
    ps_max = max_increased

    res_min = []
    init_min = 1
    for i in ps_min:
        init_min = init_min * i
        res_min.append(init_min)
    lower_bound = Decimal(len(in_points) * sum(res_min[2:]))

    res_max = []
    init_max = 1
    for i in ps_max:
        init_max = init_max * i
        res_max.append(init_max)
    upper_bound = Decimal(len(in_points) * sum(res_max[2:]))

    print(sqrt(len(in_points)), "{:.2E}".format(lower_bound), "{:.2E}".format(upper_bound))


if __name__ == "__main__":
    for num_points in [x ** 2 for x in range(3, 25)]:
        n = int(ceil(sqrt(num_points)))
        points = [(x, y) for x in range(n) for y in range(n)]

        graph_gen(points)
    print("End")
