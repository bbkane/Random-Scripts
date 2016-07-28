# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 21:32:46 2016

@author: Ben
"""

# This one works!!!

from collections import namedtuple

Edge = namedtuple('Edge', ['start', 'finish', 'cost'])

class Element:
    def __init__(self, item, cost):
        self.item = item
        self.cost = cost
    
    def __repr__(self):
        return 'Element(item=%r, cost=%r)' % (self.item, self.cost)

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
        frontier = []
        frontier.append(Element(start, 0))
        parents = {start: None}
        while True:
            if not frontier:
                raise NoPathException(str(start))
            # treat the list like a priority queue by sorting it by cost
            # and popping the first element
            frontier.sort(key = lambda e: e.cost)
            current_node = frontier.pop(0)
            if current_node.item == end: # We're done. Get the path and return
                path = []
                current = end
                while parents[current]:
                    path.append(current)
                    current = parents[current]
                path.append(current)
                path.reverse()
                return path
            explored.add(current_node.item)
            node_edges = {e for e in self.edges if e.start == current_node.item}
            for neighbor in node_edges:
                total_neighbor_cost = neighbor.cost + current_node.cost
                if neighbor.finish not in explored:
                    for element in frontier:
                        if element.item == neighbor.finish:
                            if element.cost > total_neighbor_cost:
                                element.cost = total_neighbor_cost
                                parents[element.item] = current_node.item
                            break
                    else: # no break (the item wasn't in the frontier)
                        frontier.append(Element(neighbor.finish, total_neighbor_cost))
                        parents[neighbor.finish] = current_node.item
                        

def main():
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
    

if __name__ == '__main__':
    main()