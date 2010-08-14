from django.contrib.sites.models import Site
from django.utils.functional import SimpleLazyObject


def site(request):
    return {
        'site': SimpleLazyObject(Site.objects.get_current),
    }
