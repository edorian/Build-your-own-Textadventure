from django.db import models
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
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_NORMAL)

    def __unicode__(self):
        return self.title

class Achievements (models.Model):
    user = models.OneToOneField("auth.User")

