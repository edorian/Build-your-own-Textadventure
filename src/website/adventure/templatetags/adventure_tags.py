import re
from BeautifulSoup import BeautifulSoup
from markdown import markdown
from django import template
from django.utils.encoding import force_unicode
from django.utils.html import mark_safe


register = template.Library()


@register.filter
def showtext(location):
    html = markdown(location.description)
    soup = BeautifulSoup(html)
    for a in soup.findAll('a', href=re.compile('^#\d+$')):
        a['href'] = location.get_location_link(a['href'])
    html = force_unicode(soup)
    return mark_safe(html)
