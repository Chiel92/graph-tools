"""This module contains algorithms for computing the maximal independent sets."""


def bron_kerbosch_mc(graph):
    """Compute all maximal cliques."""
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert include.isdisjoint(rest)
        assert include.isdisjoint(exclude)
        assert rest.isdisjoint(exclude)

        #print('{}, {}, {}'.format(include, rest, exclude))

        if not exclude and not rest:
            yield include

        for v in list(rest):
            assert not v in v.neighbours
            yield from recursion(include.union({v}),
                                 rest.intersection(set(v.neighbours)),
                                 exclude.intersection(set(v.neighbours)))
            rest.difference_update({v})
            exclude.update({v})

    yield from recursion(set(), set(graph.vertices), set())


def bron_kerbosch_mis(graph):
    """Compute all maximal independent sets."""
    def recursion(include, rest, exclude):
        assert include or exclude or rest
        assert include.isdisjoint(rest)
        assert include.isdisjoint(exclude)
        assert rest.isdisjoint(exclude)

        #print('{}, {}, {}'.format(include, rest, exclude))

        if not exclude and not rest:
            yield include

        for v in list(rest):
            assert not v in v.neighbours
            yield from recursion(include.union({v}),
                                 rest.difference(set(v.neighbours).union({v})),
                                 exclude.difference(set(v.neighbours)))
            rest.difference_update({v})
            exclude.update({v})

    yield from recursion(set(), set(graph.vertices), set())


from random import randint
from PIL import Image
from plot import plot_bipartite_graph, plot_graph
from graph import Graph
from bipartite import Bipartite

def mul_abs(x):
    return max(x, 1 / x)


def mc_vs_mis():
    """
    Compare the number of maximal cliques to the number of
    maximal independent sets.
    """
    for _ in range(20):
        nr_vertices = 20
        nr_edges = randint(0, int(nr_vertices * (nr_vertices - 1) / 2))
        graph = Graph.generate_random(nr_vertices, nr_edges)

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        mc = list(bron_kerbosch_mc(graph))
        nr_mc = len(mc)
        #print('{} - {} = {}'.format(nr_mis, nr_mc, abs(nr_mis - nr_mc)))
        print('{} / {} = {}'.format(nr_mis, nr_mc, mul_abs(nr_mis / nr_mc)))


def mis_bipartite_complement():
    """
    Compare the number of maximal independent sets to the number of maximal
    independent sets in the bipartite complement.
    """
    bound = 10
    nr_vertices = 10

    while 1:
        max_nr_edges = int((nr_vertices / 2) ** 2)
        nr_edges = randint(1, max_nr_edges - 1)
        nr_edges_compl = max_nr_edges - nr_edges
        graph = Bipartite.generate_random(nr_vertices, nr_edges)
        bipartite_compl = graph.bipartite_complement()

        mis = list(bron_kerbosch_mis(graph))
        nr_mis = len(mis)
        # print(mis)

        vertices = set(graph.vertices)
        edges = set((v, w) for v in graph.vertices for w in graph.vertices)
        compl_mis = [vertices.difference(s) for s in mis]
        # print(compl_mis)

        mis_compl = list(bron_kerbosch_mis(bipartite_compl))
        nr_mis_compl = len(mis_compl)
        #print('MIS: {}\n<-->\nMBC: {}'.format(mis, mis_compl))
        #print('MIS: {}\nMIS_compl: {}\nMBC: {}'.format(mis, compl_mis, mis_compl))
        # print('---------------------------------------')

        difference = abs(nr_mis - nr_mis_compl)
        if difference >= bound:
            print('Edges: {}, #MIS: {} | Edges_c: {}, #MIS_c : {}'.format(
                nr_edges, nr_mis,
                nr_edges_compl, nr_mis_compl
            ))

            graph.save('output/{},{}.graph'.format(nr_vertices, difference))

            size = (512, 512)
            im = Image.new('RGB', size, 'white')
            plot_bipartite_graph(im, graph, color=(178, 0, 0))
            im.save('output/test.png', 'png')

            break

        # print('{}, {}, {}, {}'.format(
            #nr_mis - nr_mis_compl,
            #round(nr_mis / nr_mis_compl, 1),
            #round((nr_mis / nr_edges) / (nr_mis_compl / nr_edges_compl), 1),
            #round((nr_mis * nr_edges) / (nr_mis_compl * nr_edges_compl), 1)
        #))
