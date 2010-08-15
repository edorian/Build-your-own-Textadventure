from django import template
from website.adventure.models import Graph

register = template.Library()


@register.inclusion_tag('adventure/graph/graph.html')
def adventure_graph(adventure, css_class=None):
    try:
        graph = adventure.graph
    except Graph.DoesNotExist:
        graph = None
    return {
        'css_class': css_class,
        'adventure': adventure,
        'graph': graph,
    }
