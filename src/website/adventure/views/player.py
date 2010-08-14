from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.db.models import Avg
from website.adventure.models import Adventure, Location, Rating


def adventure_list(request, adventures=None, extra_context=None):
    if adventures is None:
        adventures = Adventure.objects.filter(published=True)
    adventures = adventures.annotate(avg_rating=Avg('rating__rating'))

    context = {
        "adventures": adventures,
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

    if extra_context is not None:
        context.update(extra_content)

    return render_to_response('adventure/adventure_list.html', context,
        context_instance=RequestContext(request))

@login_required
def adventure_list_my(request):
    adventures = Adventure.objects.filter(author=request.user)
    return adventure_list(request, adventures, {"only_own_adventures": True});

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
    startlocation = object.locations.order_by('number')[0].number
    return adventure_location(request, object_id, startlocation, {"extra_content": startmessage})

def adventure_location(request, adventure_id, location_number, extra_context=None):
    extra_context = extra_context or {}
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    location = get_object_or_404(Location, adventure=adventure, number=location_number)
    context = {
        "adventure": adventure,
        "location": location,
    }
    if request.user.is_authenticated():
        context["RATING_CHOICES"] = Rating.RATING_CHOICES
        try:
            context["user_rating"] = Rating.objects.get(
                adventure=adventure,
                user=request.user
            )
        except Rating.DoesNotExist:
            context["user_rating"] = -1;

    context.update(extra_context)
    return render_to_response('adventure/adventure_location.html', context,
        context_instance=RequestContext(request))

@login_required
def adventure_rating(request, adventure_id):
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    rating, created = Rating.objects.get_or_create(adventure=adventure, user=request.user, defaults={"rating": -1})

    try:
        if rating.rating != int(request.POST["rating"]):
            rating.rating = int(request.POST["rating"])
            rating.save();
            return HttpResponse("update")
        return HttpResponse("ok")
    except (ValueError, KeyError):
        return HttpResponse("error", status_code=401);


