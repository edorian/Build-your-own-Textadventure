from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404 
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404
from website.adventure.models import Adventure, Location


def adventure_list(request):
    adventures = Adventure.objects.filter(published=True)
    context = {
        "adventures": adventures
    }
    if request.user.is_authenticated():
        context["show_status"] = True
        completed_adventures = set(
            request.user.completed_adventure.all() & adventures
        )
        started_adventures = set(
            request.user.started_adventure.all() & adventures
        )
        for adventure in adventures:
            if(adventure in completed_adventures):
                adventure.status = "completed"
            elif(adventure in started_adventures):
                adventure.status = "played"
            else:
                adventure.status = "unplayed"


    return render_to_response('adventure/adventure_list.html', context,
        context_instance=RequestContext(request))

@login_required
def adventure_list_my(request):
    objects = Adventure.objects.filter(author=request.user)
    return render_to_response('adventure/adventure_list.html', {
        "adventures": objects,
        "only_own_adventures": True,
    }, context_instance=RequestContext(request))

def adventure_detail(request, object_id):
    object = Adventure.objects.get(pk=object_id)
    return render_to_response('adventure/adventure_detail.html', {
        "object": object,
    }, context_instance=RequestContext(request))

def adventure_start(request, object_id):
    queryset = Adventure.objects.public(request)
    object = get_object_or_404(queryset, pk=object_id)

    if request.user.is_authenticated():
        if not object.started_by_user.filter(pk=request.user.id).exists():
            object.started_by_user.add(request.user)

    startmessage = render_to_string('adventure/adventure_start.html', {
        "object": object_id,
    }, context_instance=RequestContext(request))
    startlocation = object.locations.order_by('number')[0].pk
    return adventure_location(request, object_id, startlocation, {"extra_content": startmessage})

def adventure_location(request, adventure_id, location_id, extra_context=None):
    extra_context = extra_context or {}
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    location = get_object_or_404(Location, adventure=adventure, pk=location_id)
    context = {
        "adventure": adventure,
        "location": location,
    }
    context.update(extra_context)
    return render_to_response('adventure/adventure_location.html', context,
        context_instance=RequestContext(request))
