import hashlib
import tempfile
from django.conf import settings
from django.core.files import File
from django.db.models.signals import post_save
from pygraphviz import AGraph
from website.adventure.models import Location, Graph


class GraphGenerator(object):
    def __init__(self, adventure):
        self.adventure = adventure
        self.locations = list(adventure.locations.all())
        self.graph = None
        self.win_locations = set([
            l.get_number_display()
            for l in self.locations
            if l.type == l.TYPE_WIN])
        self.loose_locations = set([
            l.get_number_display()
            for l in self.locations
            if l.type == l.TYPE_LOOSE])

    def format_win_node(self, node):
        node.attr['style'] = 'filled'
        node.attr['fillcolor'] = '#ddffdd'
        node.attr['color'] = 'green'

    def format_loose_node(self, node):
        node.attr['style'] = 'filled'
        node.attr['fillcolor'] = '#ffffdd'
        node.attr['color'] = '#888800'

    def format_loose_end(self, node):
        node.attr['color'] = '#ff0000'
        node.attr['fontcolor'] = '#ff0000'

    def format_start_node(self, node):
        node.attr['style'] = 'filled'
        node.attr['fillcolor'] = '#ddddff'
        node.attr['color'] = '#0000ff'

    def generate_location_graph(self):
        graph = AGraph(strict=False, directed=True)
        graph.add_nodes_from([l.get_number_display() for l in self.locations])
        for location in self.locations:
            for link in location.links.all():
                graph.add_edge(
                    location.get_number_display(),
                    link.get_number_display())
        self.graph = graph

    def color_graph(self):
        if len(self.locations) == 0:
            return

        loose_ends = set([l.get_number_display() for l in self.locations])
        loose_ends -= self.win_locations
        loose_ends -= self.loose_locations
        for u, v in self.graph.edges_iter():
            loose_ends -= set([u])
            if not loose_ends:
                break
        for node in loose_ends:
            node = self.graph.get_node(node)
            self.format_loose_end(node)

        starting_location = self.locations[0].get_number_display()
        start_node = self.graph.get_node(starting_location)
        self.format_start_node(start_node)

        for node in self.win_locations:
            node = self.graph.get_node(node)
            self.format_win_node(node)

        for node in self.loose_locations:
            node = self.graph.get_node(node)
            self.format_loose_node(node)

    def get_hash(self):
        sha = hashlib.sha1()
        # fill hash with dot file data
        sha.update(self.graph.string())
        return sha.hexdigest()


def update_location_graph(sender, instance, **kwargs):
    generator = GraphGenerator(instance.adventure)
    generator.generate_location_graph()
    generator.color_graph()
    generator.get_hash()
    graph, created = Graph.objects.get_or_create(adventure=instance.adventure)
    graph.hash = generator.get_hash()
    graph.dot = generator.graph.string()

    handle, filename = tfile = tempfile.mkstemp(suffix='.svg')
    generator.graph.draw(filename, 'svg', 'dot')
    svg = graph.svg.storage.save('adventures/graphs/%s.svg' % graph.hash, File(open(filename, 'rb')))
    if graph.svg:
        graph.svg.storage.delete(graph.svg)
    graph.svg = svg
    graph.save()


post_save.connect(update_location_graph, sender=Location)
