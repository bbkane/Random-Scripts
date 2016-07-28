# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 21:32:46 2016

@author: Ben
"""

# This one works!!!

from collections import namedtuple

class PriorityQueue:

    class Element:
        def __init__(self, item, cost):
            self.item = item
            self.cost = cost

        def __iter__(self):
            yield self.item
            yield self.cost
        
        def __repr__(self):
            return 'Element(item=%r, cost=%r)' % (self.item, self.cost)
    
    def __init__(self):
        self._list = []

    def push(self, item, cost):
        self._list.append(type(self).Element(item, cost))
        self._list.sort(key = lambda e: e.cost)

    def pop(self):
        return self._list.pop(0)
    
    def __iter__(self):
        yield from (e for e in self._list)
        self._list.sort(key= lambda e: e.cost)
        
    def __bool__(self):
        return bool(self._list)
        
    def __str__(self):
        return '[' + '\n'.join(str(e) for e in self._list) + ']'

Edge = namedtuple('Edge', ['start', 'finish', 'cost'])

class Edge1:
    def __init__(self, start, finish, cost):
        self.start = start
        self.finish = finish
        self.cost = cost

    def __hash__(self):
        return(hash((self.start, self.finish, self.cost)))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.start == other.start and \
            self.finish == other.finish and self.cost == other.cost
    
    def __repr__(self):
        return 'Edge(start=%r, finish=%r, cost=%r)' % \
            (self.start, self.finish, self.cost)

class NoPathException(Exception):
    pass

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()
        
    def add_two_way(self, a, b, cost):
        self.nodes.add(a)
        self.nodes.add(a)
        self.edges.add(Edge(b, a, cost))
        self.edges.add(Edge(a, b, cost))

    def __str__(self):
        node_str=  'nodes:\n' + '\n'.join(str(node) for node in self.nodes)
        edge_str = 'edges:\n' + '\n'.join(str(edge) for edge in self.edges)
        return node_str + '\n' + edge_str

    def dijkstra(self, start, end):
        explored = set()
        frontier = PriorityQueue()
        frontier.push(start, 0)
        parents = {start: None}
        while True:
            if not frontier:
                raise NoPathException(str(start))
            node, node_cost = frontier.pop()
            print('current node:', node)
            if node == end:
                current = end
                while parents[current]:
                    print(current)
                    current = parents[current]
                print(current)
                return
            explored.add(node)
            node_edges = {e for e in self.edges if e.start == node}
            for neighbor in node_edges:
                print('neighbor:', neighbor.finish)
                if neighbor.finish not in explored:
                    in_frontier = False
                    for element in frontier:
                        if element.item == neighbor.finish:
                            if element.cost > neighbor.cost + node_cost:
                                element.cost = neighbor.cost + node_cost
                                parents[element.item] = node
                            in_frontier = True
                    if not in_frontier:
                        frontier.push(neighbor.finish, neighbor.cost + node_cost)
                        parents[neighbor.finish] = node
                        
# # start djikstra
# explored = set()
# frontier = []
# start_node = Node(parent=None, cost=0)
# frontier.append(start_node)
# while True:
#     if not frontier:
#         return None
#     sorted(frontier, key=n.cost)
#     node = frontier.pop()
#     if is_goal(node):
#         return True
#     explored.add(node)
#     for neighbor in neighbors(node):
#         if neighbor not in explored:
#             if neighbor not in frontier:
#                 neighbor.parent = node
#                 neighbor.cost = node.cost + cost_from(node, neighbor)
#                 frontier.append(neighbor)
#             else:
#                 neighbor_in_frontier = get_from_frontier(node)
#                 if neighbor.cost < neighbor_in_frontier.cost:
#                     neighbor_in_frontier.cost = neighbor.cost
#                     neighbor_in_frontier.parent = neighbor.parent

g = Graph()

g.add_two_way('1', '2', 7)
g.add_two_way('1', '3', 9)
g.add_two_way('1', '6', 14)
g.add_two_way('2', '3', 10)
g.add_two_way('2', '4', 15)
g.add_two_way('3', '4', 11)
g.add_two_way('3', '6', 2)
g.add_two_way('4', '5', 6)
g.add_two_way('5', '6', 9)

print(g)

print(g.dijkstra('1', '5'))

