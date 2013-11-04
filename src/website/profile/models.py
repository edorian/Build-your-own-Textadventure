from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField('auth.User')

    def __unicode__(self):
        return self.user.username

    @models.permalink
    def get_absolute_url(self):
        return 'profile', (), {}


def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def sync_profiles(sender, created_models, **kwargs):
    if Profile in created_models:
        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)


models.signals.post_save.connect(create_profile_for_user, sender=User)
models.signals.post_syncdb.connect(sync_profiles)
