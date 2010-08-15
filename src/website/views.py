from django.shortcuts import render_to_response
from django.template import RequestContext
from website.adventure.models import Adventure
from django.db.models import Avg, Count

def index(request):
#    adventures = Adventure.objects.filter(published=True)
#    adventures = adventures.annotate(avg_rating=Avg('rating__rating'))
#    adventures = adventures.annotate(ratings=Count('rating__rating'))

#    adventures.filter(ratings__gte=Adventure.RATINGS_REQUIRED_TO_CARE).order_by('avg_rating')[:5]
    
    context = {
#        "popular_adventures": adventures,
#        "random_adventure": 
    }

    return render_to_response('index.html', context,
        context_instance=RequestContext(request))


def about(request):
    return render_to_response('about.html', {
    }, context_instance=RequestContext(request))
