#! /usr/bin/env python

from __future__ import division
from math import ceil, floor, sqrt
from math import factorial as fact
from itertools import combinations
from collections import Counter
from decimal import Decimal

init_res_num = 4 # 4 ~ fin_res_num
fin_res_num = 25 # under 25 can be used.

# get_points and gen_points_dic to calculate ps
def get_points(point1, point2):
        points = set()

        if point1[0] == point2[0]:
                if point1[1] < point2[1]: return set([(point1[0], y) for y in range(point1[1]+1, point2[1])])
                else: return set([(point1[0], y) for y in range(point2[1]+1,point1[1])])
        if point1[1] == point2[1]:
                if point1[0] < point2[0]: return set([(x, point1[1]) for x in range(point1[0]+1, point2[0])])
                else: return set([(x, point1[1]) for x in range(point2[0]+1,point1[0])])

        xs = []
        ys = []
        if point1[0] < point2[0]: xs = range(point1[0]+1, point2[0])
        else: xs = range(point2[0]+1, point1[0])
        if point1[1] < point2[1]: ys = range(point1[1]+1, point2[1])
        else: ys = range(point2[1]+1, point1[1])

        for point in [(x,y) for x in xs for y in ys]:
                if point[1] - point1[1] == (point[0] - point1[0])*((point2[1]-point1[1])/(point2[0]-point1[0])):
                        points.add(point)

        return points

def graph_gen(points):
        vertices = []
        order_two = combinations(points, 2)

        for point1, point2 in order_two:
                middles = get_points(point1, point2)
                if middles == set(): vertices.append((point1, point2))

        graph = {}
        for vertice in vertices:
                if graph.has_key(vertice[0]): graph[vertice[0]] = graph[vertice[0]]+1
                else: graph[vertice[0]] = 1
                if graph.has_key(vertice[1]): graph[vertice[1]] = graph[vertice[1]]+1
                else: graph[vertice[1]] = 1

        min_val = min(graph.itervalues())
        max_val = max(graph.itervalues())

        min_points = []
        for point, value in graph.iteritems():
                if value == min_val:
                        min_points.append(point)
        min_grads = []
        for i in points:
                if i == min_points[0]: continue
                if i[0] == min_points[0][0]: grad = float("inf")
                else: grad = (i[1]-min_points[0][1])/(i[0]-min_points[0][0])
                min_grads.append(grad)
        sorted_grad = [y for x,y in Counter(min_grads).most_common()]

        init = 1
        ps_min = []
        for i in sorted_grad:
                ps_min = ps_min + [init]*i
                init = init + 1
        ps_min.reverse()

        min_decreased = range(min_val, 0, -1)
        min_decreased = min_decreased + [1] * (len(points) - len(min_decreased) - 1)
        ps_min = [max(x) for x in zip(ps_min, min_decreased)]

        max_increased = range(max_val, 0, -1)
        max_increased = [max_val] * (len(points) - len(max_increased) - 1) + max_increased
        ps_max = max_increased

        res_min = []
        init_min = 1
        for i in ps_min:
                init_min = init_min * i
                res_min.append(init_min)
        lower_bound = Decimal(len(points) * sum(res_min[2:]))

        res_max = []
        init_max = 1
        for i in ps_max:
                init_max = init_max * i
                res_max.append(init_max)
        higher_bound = Decimal(len(points) * sum(res_max[2:]))

        MINCOL = '\033[91m'
        MAXCOL = '\033[92m'
        ENDC = '\033[0m'

        width = int(ceil(sqrt(len(points))))
        print len(points), min_val, max_val, "{:.2E}".format(lower_bound), "{:.2E}".format(
                higher_bound), "{:.2E}".format((lower_bound*higher_bound).sqrt())

        #       if True or min_val != graph[(0,0)]:
        #               for i in range(width):
        #                       row = []
        #                       for j in range(width):
        #                               if graph.has_key((i,j)):
        #                                       if graph[(i,j)] == min_val:
        #                                               row.append(MINCOL + str(graph[(i,j)]) + ENDC)
        #                                       elif graph[(i,j)] == max_val:
        #                                               row.append(MAXCOL + str(graph[(i,j)]) + ENDC)
        #                                       else:
        #                                               row.append(str(graph[(i,j)]))
        #                               else: row.append("X")
        #                       print('\t'.join(map(str,row)))
        #               print ""


def path_calc(idx, i_graph):
        degrees = i_graph.degree()
        paths = []
        paths.append(2 * len(degrees))

        for path_len in range(1, idx - 1):
                paths.append(lower_bound(path_len, i_graph.copy()))

        return paths


if __name__ == "__main__":
        # graph generation
        graph_list = []
        for num_points in [x ** 2 for x in range(2, 200)]:
                n = int(ceil(sqrt(num_points)))
                points = [(x, y) for x in range(n) for y in range(n)]
                new_point = None

                graph_gen(points)
        # raw_input("> ")
        print "End"

