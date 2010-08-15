from django import template

register = template.Library()


@register.inclusion_tag('adventure/graph/graph.html')
def adventure_graph(adventure, css_class=None):
    return {
        'css_class': css_class,
        'adventure': adventure,
        'graph': adventure.graph,
    }
