from website.adventure.models import Adventure, Location
from django.shortcuts import render_to_response, get_object_or_404 
from django.template.loader import render_to_string
from django.template import RequestContext

def adventure_list(request):
    objects = Adventure.objects.filter(published=True)
    return render_to_response('adventure/adventure_list.html', {
        "object_list": objects,
    }, context_instance=RequestContext(request))

def adventure_detail(request, object_id):
    object = Adventure.objects.get(pk=object_id)
    return render_to_response('adventure/adventure_detail.html', {
        "object": object,
    }, context_instance=RequestContext(request))

def adventure_start(request, object_id):
    startmessage = render_to_string('adventure/adventure_start.html', {
        "object": object_id,
    }, context_instance=RequestContext(request))
    startlocation = 1; # default start location for now
    return adventure_location(request, object_id, startlocation, {"extra_content": startmessage})

def adventure_location(request, adventure_id, location_id, extra_context=None):
    extra_context = extra_context or {}
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    location = get_object_or_404(Location, pk=location_id)
    context = {
        "adventure": adventure,
        "location": location,
    }
    context.update(extra_context)
    return render_to_response('adventure/adventure_location.html', context,
        context_instance=RequestContext(request))


