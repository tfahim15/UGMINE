import copy
import tracemalloc

import sys
sys.setrecursionlimit(15000)
tracemalloc.start()
external_utility = dict()

class InputGraph:
    def __init__(self):
        self.vertices = []
        self.edges = []
        self.adjacency = dict()
        self.dfs_order = dict()
        self.time = 0

    def dfs_visit(self, u):
        self.dfs_order[u] = self.time
        self.time += 1
        try:
            _ = self.adjacency[u]
        except KeyError:
            return
        for v in self.adjacency[u]:
            if self.dfs_order[v] == -1:
                self.dfs_visit(v)

    def __repr__(self) -> str:
        return "\nVertices:" + str(self.vertices) + "\nEdges: " + str(self.edges) \
               + "\nDFS order: " + str(self.dfs_order) + "\nAdjacency List: " + str(self.adjacency) + "\n"


class Graph:
    def __init__(self):
        self.vertices = dict()
        self.adjacency = dict()
        self.utility = -float('inf')

    def graph_utility(self):
        if self.utility > -float('inf'):
            return self.utility
        utility = 0.0
        for u in self.adjacency:
            for e in self.adjacency[u]:
                v, edge_label, internal_utility = e
                if u > v:
                    continue
                u_label = self.vertices[u]
                v_label = self.vertices[v]
                if u_label <= v_label:
                    utility += internal_utility * external_utility[(u_label, v_label, edge_label)]
                else:
                    utility += internal_utility * external_utility[(v_label, u_label, edge_label)]
        self.utility = utility
        return utility

    def __repr__(self) -> str:
        return "\nVertices:" + str(self.vertices) \
               + "\nAdjacency List: " + str(self.adjacency) + "\n"


input_graphs =[]

file = open("NCI1log.txt").readlines()
mode = -1
for line in file:
    if line[0] == 't':
        mode += 1
        input_graphs.append(InputGraph())
        continue
    elif mode == -1:
        vertex1, vertex2, edge, utility = line.split(" ")
        vertex1 = int(vertex1)
        vertex2 = int(vertex2)
        edge = int(edge)
        utility = float(utility)
        external_utility[(vertex1, vertex2, edge)] = utility
    elif line[0] == 'v':
        _, vertex, label = line.split(" ")
        vertex = int(vertex)
        label = int(label)
        input_graphs[mode].vertices.append((vertex,label))
        input_graphs[mode].dfs_order[vertex] = -1
    elif line[0] == 'e':
        _, vertex1, vertex2, label, utility = line.split(" ")
        vertex1 = int(vertex1)
        vertex2 = int(vertex2)
        label = int(label)
        utility = float(utility)
        if vertex1 in input_graphs[mode].adjacency:
            input_graphs[mode].adjacency[vertex1].append(vertex2)
        else:
            input_graphs[mode].adjacency[vertex1] = [vertex2]
        if vertex2 in input_graphs[mode].adjacency:
            input_graphs[mode].adjacency[vertex2].append(vertex1)
        else:
            input_graphs[mode].adjacency[vertex2] = [vertex1]

        input_graphs[mode].edges.append((vertex1, vertex2, label, utility))


graphs = []
cc=1
for g in input_graphs:
    print(cc)
    cc+=1
    for v, _ in g.vertices:
        if g.dfs_order[v] == -1:
            g.dfs_visit(v)
    graph = Graph()
    for v in g.vertices:
        graph.vertices[g.dfs_order[v[0]]] = v[1]
    for e in g.edges:
        if g.dfs_order[e[0]] in graph.adjacency:
            graph.adjacency[g.dfs_order[e[0]]].append((g.dfs_order[e[1]], e[2], e[3]))
        else:
            graph.adjacency[g.dfs_order[e[0]]] = [(g.dfs_order[e[1]], e[2], e[3])]
        if g.dfs_order[e[1]] in graph.adjacency:
            graph.adjacency[g.dfs_order[e[1]]].append((g.dfs_order[e[0]], e[2], e[3]))
        else:
            graph.adjacency[g.dfs_order[e[1]]] = [(g.dfs_order[e[0]], e[2], e[3])]
    graphs.append(graph)

min_util = 0.0
for g in graphs:
    min_util += g.graph_utility()
    print(g.graph_utility())
min_util *= 0.09
print("----------------------------------")
print(min_util)

def RightMostPath(code):
    adj = dict()
    ur = 0
    for c in code:
        ur = max(ur, c[0])
        ur = max(ur, c[1])
        if c[1] > c[0]:
            adj[c[1]] = c[0]
    result = [ur]
    u = ur
    while u != 0:
        u = adj[u]
        result.append(u)
    return ur, list(reversed(result))


def get_utility(code, graph, isomorphism):
    result = 0.0
    for c in code:
        ext_utility = 0.0
        u, v, u_label, v_label, edge_label = c
        if u_label < v_label:
            ext_utility = external_utility[(u_label, v_label, edge_label)]
        else:
            ext_utility = external_utility[(v_label, u_label, edge_label)]
        iso_u, iso_v = isomorphism[u], isomorphism[v]
        int_utility = 0.0
        for e in graph.adjacency[iso_u]:
            if e[0] == iso_v and e[1] == edge_label:
                int_utility = e[2]
        result += ext_utility*int_utility
    return result


def RightMostExtensions(code, graphs):
    result = dict()
    for i in range(len(graphs)):
        graph = graphs[i]
        temp_result = dict()
        if code.__len__() == 0:
            for u in graph.adjacency:
                for e in graph.adjacency[u]:
                    v, edge_label, internal_utility = e
                    u_label = graph.vertices[u]
                    v_label = graph.vertices[v]
                    utility = 0.0
                    if u_label < v_label:
                        utility = internal_utility * external_utility[(u_label, v_label, edge_label)]
                    else:
                        utility = internal_utility * external_utility[(v_label, u_label, edge_label)]
                    if (0, 1, u_label, v_label, edge_label) in temp_result:
                        temp_result[(0, 1, u_label, v_label, edge_label)] = max(utility, temp_result[(0, 1, u_label, v_label, edge_label)])
                    else:
                        temp_result[(0, 1, u_label, v_label, edge_label)] = utility
        else:
            isomorphisms = subgraphIsomorphisms(code, graph)
            u, R = RightMostPath(code)
            for isomorphism in isomorphisms:
                for v in R:
                    if u == v:
                        continue
                    iso_u = isomorphism[u]
                    iso_v = isomorphism[v]
                    for e in graph.adjacency[iso_u]:
                        if e[0] != iso_v:
                            continue
                        edge_label = e[1]
                        exists = False
                        for c in code:
                            if c[0] == u and c[1] == v and c[4] == edge_label:
                                exists = True
                            elif c[0] == v and c[1] == u and c[4] == edge_label:
                                exists = True
                        if not exists:
                            new_code = copy.deepcopy(code)
                            new_code.append((u, v, graph.vertices[iso_u], graph.vertices[iso_v], edge_label))
                            utility = get_utility(new_code, graph, isomorphism)
                            if (u, v, graph.vertices[iso_u], graph.vertices[iso_u], edge_label) in temp_result:
                                temp_result[(u, v, graph.vertices[iso_u], graph.vertices[iso_v], edge_label)] = max(utility, temp_result[(u, v, graph.vertices[iso_v], graph.vertices[iso_v], edge_label)])
                            else:
                                temp_result[(u, v, graph.vertices[iso_u], graph.vertices[iso_v], edge_label)] = utility
                ur = u
                for u in R:
                    iso_u = isomorphism[u]
                    for e in graph.adjacency[iso_u]:
                        iso_v, edge_label, int_utility = e
                        if iso_v in isomorphism.values():
                            continue
                        u_label, v_label = graph.vertices[iso_u], graph.vertices[iso_v]
                        new_code = copy.deepcopy(code)
                        new_code.append((u, ur + 1, u_label, v_label, edge_label))
                        isomorphism_ = copy.deepcopy(isomorphism)
                        isomorphism_[ur + 1] = iso_v
                        utility = get_utility(new_code, graph, isomorphism_)
                        if (u, ur+1, u_label, v_label, edge_label) in temp_result:
                            temp_result[(u, ur+1, u_label, v_label, edge_label)] = max(utility,temp_result[(u, ur+1, u_label, v_label, edge_label)])
                        else:
                            temp_result[(u, ur+1, u_label, v_label, edge_label)] = utility

        for key in temp_result:
            if key in result:
                utility, gwu = result[key]
                result[key] = (temp_result[key] + utility, gwu + graph.graph_utility())
            else:
                result[key] = (temp_result[key], graph.graph_utility())
    return result


def buildGraph(code):
    graph = Graph()
    for tuple in code:
        u, v, u_label, v_label, edge_label = tuple
        graph.vertices[u] = u_label
        graph.vertices[v] = v_label
        if u in graph.adjacency:
            graph.adjacency[u].append((v, edge_label, 0.0))
        else:
            graph.adjacency[u] = [(v, edge_label, 0.0)]
        if v in graph.adjacency:
            graph.adjacency[v].append((u, edge_label, 0.0))
        else:
            graph.adjacency[v] = [(u, edge_label, 0.0)]
    return graph


def minTuple(tuple1, tuple2):
    u1, v1, u1_label, v1_label, edge1label = tuple1
    u2, v2, u2_label, v2_label, edge2label = tuple2
    if u1 == u2 and v1 == v2:
        if u1_label < u2_label:
            return tuple1
        elif u1_label > u2_label:
            return tuple2
        elif v1_label < v2_label:
            return tuple1
        elif v1_label > v2_label:
            return tuple2
        elif edge1label < edge2label:
            return tuple1
        return tuple2
    else:
        if u1 < v1 and u2 < v2:  # both forward edge
            if v1 < v2:
                return tuple1
            elif v1 == v2 and u1 > u2:
                return tuple1
            return tuple2
        if u1 > v1 and u2 > v2:  # both backward edge
            if u1 < u2:
                return tuple1
            elif u1 == u2 and v1 < v2:
                return tuple1
            return tuple2
        if u1 < v1 and u2 > v2:  # tuple1 forward tuple2 backward
            if v1 <= u2:
                return tuple1
            return tuple2
        if u1 > v1 and u2 < v2:  # tuple1 backward tuple2 forward
            if u1 < v2:
                return tuple1
            return tuple2


def minExtension(tuples):
    result = None
    for t in tuples:
        if result is None:
            result = t
        else:
            result = minTuple(result, t)
    return result


def isCannonical(code):
    graph = buildGraph(code)
    c = []
    for i in range(len(code)):
        extension = minExtension(RightMostExtensions(c, [graph]))
        if minTuple(extension, code[i]) != code[i]:
            return False
        c.append(extension)
    return True


def subgraphIsomorphisms(code, graph):
    isomorphisms = []
    l0 = code[0][2]
    for v in graph.vertices:
        if graph.vertices[v] == l0:
            isomorphisms.append({0: v})
    for tuple in code:
        u, v, u_label, v_label, edge_label = tuple
        temp_isomorphisms = []
        for isomorphism in isomorphisms:
            if v > u:
                iso_u = isomorphism[u]
                try:
                    _ = graph.adjacency[iso_u]
                except KeyError:
                    continue
                for e in graph.adjacency[iso_u]:
                    iso_v, iso_edge_label, _ = e
                    if iso_v not in isomorphism.values() and graph.vertices[iso_v] == v_label and edge_label == iso_edge_label:
                        new_iso = copy.deepcopy(isomorphism)
                        new_iso[v] = iso_v
                        temp_isomorphisms.append(new_iso)
            else:
                iso_u = isomorphism[u]
                iso_v = isomorphism[v]
                for e in graph.adjacency[iso_u]:
                    c_iso_v, c_iso_edge_label, _ = e
                    if c_iso_v == iso_v and edge_label == c_iso_edge_label:
                        temp_isomorphisms.append(copy.deepcopy(isomorphism))
        isomorphisms = temp_isomorphisms
    return isomorphisms

import time

hup, candidates= 0, 0
def GSpan(code, graphs, min_util, t):
    global hup, candidates
    code = copy.deepcopy(code)
    extentions = RightMostExtensions(code, graphs)
    for key in extentions:
        utility, gwu = extentions[key]
        new_code = copy.deepcopy(code)
        new_code.append(key)
        print(time.time()-t)
        if isCannonical(new_code) and gwu > min_util:
            if utility > min_util:
                print(new_code, utility, gwu, isCannonical(new_code))
                hup += 1
            GSpan(new_code, graphs, min_util, t)


t = time.time()
GSpan([], graphs, min_util, t)
print(" ", time.time() - t, hup, candidates)
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
tracemalloc.stop()
print(5)