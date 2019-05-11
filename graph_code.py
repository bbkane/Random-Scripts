import functools
import operator


def simple_repr(cls):
    """simple repr for a class"""
    return '%s(%s)' % (type(cls).__name__, str(vars(cls)))


class Node:

    def __init__(self, value, deps=None):
        self.value = value
        self.deps = deps or []

    def _get_all_deps(self):
        """ yields all children with possible duplicates
        Notes:
            This is an underscored method because it does no checking whatsoever
            and is usually not what the user wants
        """

        for dep in self.deps:
            yield from dep._get_all_deps()
            yield dep

    def topological_sort(self):
        """return a topologically sorted list of dependencies

        Notes:
            This shouldn't be a generator function because
            if it were, callers could modify the nodes before the
            sort finishes
        """

        seen = set()
        sorted_nodes = []
        for dep in self._get_all_deps():
            if dep not in seen:
                sorted_nodes.append(dep)
                seen.add(dep)

        sorted_nodes.append(self)
        return sorted_nodes

    def __hash__(self):
        """
        Notes:
            Hashing the same dependency twice means they will cancel each other out.
        return hash(self.value) ^ functools.reduce(operator.xor, map(hash, self.deps))
        won't work because of this
            Recursive hash function :(
        """
        if not self.deps:
            return hash(self.value)
        hash_set = set()
        for dep in self._get_all_deps():
            hash_set.add(dep.value)

        return hash(self.value) ^ functools.reduce(operator.xor, map(hash, hash_set))

    def __eq__(self, other):
        """
        Notes:
            Recursive equals function :(
        """
        return self.value == other.value and self.deps == other.deps

    def __repr__(self):
        """
        Notes:
            Recursive repr function :(
        """
        return simple_repr(self)


# Below this is the test code
# It seems to work
# TODO: make clearer testing 'framework'
# TODO: test equality and add more tests
class Graph:
    """Just a bag of nodes

    Mostly for testing purposes
    """
    def __init__(self, nodes=None):
        self.nodes = nodes or []

    def add(self, node):
        """Add and return a node

        Steve, this is only for testing. Don't crucify me here :)
        """
        self.nodes.append(node)
        return node


def make_graph1():
    graph = Graph()
    A = graph.add(Node('A'))
    B = graph.add(Node('B', deps=[A]))
    C = graph.add(Node('C', deps=[B]))
    D = graph.add(Node('D'))
    return graph


def make_graph2():
    graph = Graph()
    F = graph.add(Node('F'))
    E = graph.add(Node('E', deps=[F]))
    A = graph.add(Node('A'))
    B = graph.add(Node('B', deps=[E, A]))
    C = graph.add(Node('C', deps=[A]))
    D = graph.add(Node('D', deps=[B, C]))
    return graph


def test_graph(graph, index=0):
    first_hashes = [(node.value, hash(node)) for node in graph.nodes]

    graph.nodes[index].value = graph.nodes[index].value + 'changed'

    second_hashes = [(node.value, hash(node)) for node in graph.nodes]

    for n in range(len(graph.nodes)):
        if first_hashes[n][1] != second_hashes[n][1]:
            print('hash change! values:', first_hashes[n][0], second_hashes[n][0])
        else:
            print('hash constant. value:', first_hashes[n][0])


if __name__ == "__main__":
    test_graph(make_graph1(), 0)
    print()
    test_graph(make_graph2(), 2)
