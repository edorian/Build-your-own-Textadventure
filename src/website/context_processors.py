from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.functional import SimpleLazyObject


def site(request):
    return {
        'site': SimpleLazyObject(Site.objects.get_current),
    }


def piwik(request):
    return {
        'PIWIK_BASE_URL': settings.PIWIK_BASE_URL,
    }
