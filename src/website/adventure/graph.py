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
        pass

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
