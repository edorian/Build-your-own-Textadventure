from django.db import models
from django.db.models import Max
from datetime import datetime
from django.db.models import Q
from website.adventure.utils import LANGUAGES


class AdventurePublicManager(models.Manager):
    def public(self, request):
        if request.user.is_authenticated():
            return self.filter(Q(published=True) | Q(author=request.user))
        return self.filter(published=True)


class Adventure (models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey("auth.User")
    created = models.DateTimeField(default=datetime.now)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    language = models.CharField(max_length=5, choices=LANGUAGES, default="en")
    
    started_by_user = models.ManyToManyField(
        "auth.User", related_name="started_adventure", blank=True
    )
    completed_by_user = models.ManyToManyField(
        "auth.User", related_name="completed_adventure", blank=True
    )

    objects = AdventurePublicManager()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'adventure-detail', (self.pk,), {}

class Location (models.Model):
    TYPE_NORMAL = 0
    TYPE_WIN = 1
    TYPE_LOOSE = 2
    TYPE_CHOICES = (
         (TYPE_NORMAL, 'Normal'),
         (TYPE_WIN, 'Win'),
         (TYPE_LOOSE, 'Loose'),
    )

    adventure = models.ForeignKey("adventure.Adventure", related_name='locations')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_NORMAL)

    def __unicode__(self):
        return self.title

    def get_next_number(self):
        if not hasattr(self, '_next_number'):
            if self.adventure is None:
                self._next_number = 1
            else:
                aggregate = self.adventure.locations.aggregate(Max('number'))
                self._next_number = aggregate['number__max'] + 1
        return self._next_number

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self.get_next_number()
        return super(Location, self).save(*args, **kwargs)

class Achievements (models.Model):
    user = models.OneToOneField("auth.User")

