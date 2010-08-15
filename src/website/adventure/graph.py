from pygraphviz import AGraph


def generate_location_graph(adventure):
    graph = AGraph(strict=False, directed=True)
    locations = list(adventure.locations.all())
    graph.add_nodes_from([l.get_number_display() for l in locations])
    for location in locations:
        for link in location.links.all():
            graph.add_edge(
                location.get_number_display(),
                link.get_number_display())
    return graph
