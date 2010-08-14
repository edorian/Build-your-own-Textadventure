from django.db import models
from datetime import datetime

class Adventure (models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey("auth.User")
    created = models.DateTimeField(default=datetime.now)
    description = models.TextField(blank=True)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

class Location (models.Model):
    TYPE_NORMAL = 0
    TYPE_WIN = 1
    TYPE_LOOSE = 2
    TYPE_CHOICES = (
        (TYPE_NORMAL, 'Normal'),
        (TYPE_WIN, 'Win'),
        (TYPE_LOOSE, 'Loose'),
    )

    adventure = models.ForeignKey("adventure.Adventure")
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=TYPE_NORMAL)

    def __unicode__(self):
        return self.title
