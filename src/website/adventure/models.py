import re
from datetime import datetime
from BeautifulSoup import BeautifulSoup
from markdown import markdown
from django.core.urlresolvers import get_resolver, reverse, Resolver404
from django.db import models
from django.db.models import Max
from django.db.models import Q, Avg
from django.utils.encoding import force_unicode
from django.utils.html import escape, mark_safe
from django_extensions.db.fields import CreationDateTimeField, \
    ModificationDateTimeField
from website.adventure.utils import LANGUAGES


class AdventurePublicManager(models.Manager):
    def public(self, request):
        if request.user.is_authenticated():
            return self.filter(Q(published=True) | Q(author=request.user))
        return self.filter(published=True)


class Adventure (models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey("auth.User")
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    language = models.CharField(max_length=5, choices=LANGUAGES, default="en")

    started_by_user = models.ManyToManyField(
        "auth.User", related_name="started_adventure", blank=True)
    completed_by_user = models.ManyToManyField(
        "auth.User", related_name="completed_adventure", blank=True)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    objects = AdventurePublicManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'adventure-detail', (self.pk,), {}

    @property
    def last_location(self):
        if not hasattr(self, '_last_location'):
            try:
                self._last_location = self.locations.order_by('-number')[0]
            except IndexError:
                self._last_location = None
        return self._last_location

    @property
    def first_location(self):
        if not hasattr(self, '_first_location'):
            try:
                self._first_location = self.locations.order_by('number')[0]
            except IndexError:
                self._first_location = None
        return self._first_location

    @property
    def location_numbers(self):
        if not hasattr(self, '_location_numbers'):
            self._location_numbers = self.locations.values_list('number', flat=True)
        return self._location_numbers


class Location (models.Model):
    TYPE_NORMAL = 0
    TYPE_WIN = 1
    TYPE_LOOSE = 2
    TYPE_CHOICES = (
         (TYPE_NORMAL, 'Normal'),
         (TYPE_WIN, 'Win'),
         (TYPE_LOOSE, 'Loose'),
    )

    LOCATION_LINK_RE = re.compile(r'^#(\d+)$')

    adventure = models.ForeignKey("adventure.Adventure", related_name='locations')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_NORMAL)
    links = models.ManyToManyField('self', symmetrical=False, blank=True)

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        ordering = ('adventure', 'number',)

    def __unicode__(self):
        return '#%s %s' % (self.number, self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'adventure-locations', (self.adventure.pk, self.number), {}

    def get_description_display(self):
        text = escape(self.description)
        html = markdown(text)
        soup = BeautifulSoup(html)
        # removing all images, they can contain javascript in the src attribute
        for img in soup.findAll('img'):
            img.extract()
        for a in soup.findAll('a'):
            a['href'] = self.get_location_link(a['href'])
            if not a['href']:
                a['class'] = 'broken'
        html = force_unicode(soup)
        return mark_safe(html)

    def get_location_link(self, link):
        match = self.LOCATION_LINK_RE.match(link)
        if not match:
            return ''
        number = match.group()[1]
        number = int(number)
        # don't show error since we don't want a broken link to ruin the whole
        # adventure -> so do gracefully display nothing :)
        if number not in self.adventure.location_numbers:
            return ''
        return reverse('adventure-location', args=(self.adventure.pk, number))

    def get_number_display(self):
        return '#%s' % self.number

    def get_next_number(self):
        if not hasattr(self, '_next_number'):
            if self.adventure is None:
                self._next_number = 1
            else:
                aggregate = self.adventure.locations.aggregate(Max('number'))
                self._next_number = (aggregate['number__max'] or 0) + 1
        return self._next_number

    def extract_links(self):
        from website.adventure.views.player import adventure_location
        resolver = get_resolver(None)
        html = self.get_description_display()
        html = BeautifulSoup(html)
        links = []
        for a in html.findAll('a'):
            try:
                callback, args, kwargs = resolver.resolve(a['href'])
                if callback is adventure_location and int(kwargs['adventure_id']) == self.adventure.pk:
                    links.append(int(kwargs['location_number']))
            except Resolver404:
                pass
        return self.adventure.locations.filter(number__in=links)

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.get_next_number()
        self.links = self.extract_links()
        return super(Location, self).save(*args, **kwargs)


class Graph(models.Model):
    adventure = models.OneToOneField(Adventure, db_index=True)
    hash = models.CharField(max_length=32)
    dot = models.TextField()
    svg = models.FileField(upload_to='adventures/graphs/')

    created = CreationDateTimeField()
    modified = ModificationDateTimeField()


class RatingManager (models.Manager):
    def avg_rating(self, adventure):
        return self.filter(adventure=adventure).aggregate(Avg('rating'))

    def ratings(self, adventure):
        return self.filter(adventure=adventure).count();


class Rating (models.Model):

    RATING_CHOICES = (
        (1, "Very Bad / Broken"),
        (2, "Bad"),
        (3, "Ok"),
        (4, "Good"),
        (5, "Very Good"),
    )

    user = models.ForeignKey("auth.User")
    adventure = models.ForeignKey("adventure.Adventure")
    rating = models.IntegerField(choices=RATING_CHOICES)

    objects = RatingManager()

    class Meta:
        unique_together = ("adventure", "user")


# hook in signals to generate graphs
import website.adventure.graph
