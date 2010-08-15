from django import template

register = template.Library()


@register.inclusion_tag('adventure/graph/graph.html')
def adventure_graph(adventure):
    return {
        'adventure': adventure,
        'graph': adventure.graph,
    }
