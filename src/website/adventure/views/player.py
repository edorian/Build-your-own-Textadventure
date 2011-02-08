from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.db.models import Avg, Count
from website.adventure.models import Adventure, Location, Rating
from website.adventure.utils import LANGUAGE_CODES, LANGUAGE_NAMES


def adventure_list(request, adventures=None, extra_context=None, template_name=None):
    if adventures is None:
        adventures = Adventure.objects.filter(published=True)
    adventures = adventures.select_related('author')
    adventures = adventures.annotate(avg_rating=Avg('rating__rating'))
    adventures = adventures.annotate(ratings=Count('rating__rating'))

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
        context.update(extra_context)

    template_names = []
    if template_name is None:
        template_names.append(template_name)
    template_names.append('adventure/adventure_list.html')
    return render_to_response(template_names, context,
        context_instance=RequestContext(request))

@login_required
def adventure_list_my(request):
    adventures = Adventure.objects.filter(author=request.user)
    return adventure_list(request, adventures,
        {"only_own_adventures": True},
        'adventure7adventure_list_my.html')

def adventure_list_by_author(request, username):
    author = get_object_or_404(User, username=username)
    adventures = Adventure.objects.filter(published=True).filter(author=author)
    return adventure_list(request, adventures,
        {"author": author, "author_list": True},
        'adventure/adventure_list_author.html')

def adventure_list_by_language(request, language):
    if language not in LANGUAGE_CODES:
        raise Http404
    language_name = LANGUAGE_NAMES[language]
    adventures = Adventure.objects.filter(published=True).filter(language=language)
    return adventure_list(request, adventures,
        {"language_code": language, "language": language_name, "language_list": True},
        'adventure/adventure_list_language.html')

def adventure_detail(request, object_id):
    object = Adventure.objects.get(pk=object_id)
    resultable = False
    if 'adventure_state' in request.session and object_id in request.session['adventure_state']:
        resumeable = True
    
    return render_to_response('adventure/adventure_detail.html', {
        "object": object,
        "resumeable": resumeable,
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

    if 'adventure_state' not in request.session:
        request.session['adventure_state'] = {}
    request.session['adventure_state'][object_id] = startlocation;

    return adventure_location(request, object_id, startlocation, {"extra_content": startmessage})

def adventure_location(request, adventure_id, location_number, extra_context=None):
    extra_context = extra_context or {}
    adventure = get_object_or_404(Adventure, pk=adventure_id)
    location = get_object_or_404(Location, adventure=adventure, number=location_number)
    context = {
        "adventure": adventure,
        "location": location,
    }

    if request.session['adventure_state'][adventure_id] != location_number:
        # User moved
        # TODO Check if move was allowed
        old_location = location_number
        new_location = location.id
        # TODO How to query that table now

        request.session['adventure_state'][adventure_id] = location_number

    if request.user.is_authenticated():
        if location.type == location.TYPE_WIN:
            if not adventure.completed_by_user.filter(pk=request.user.id).exists():
                adventure.completed_by_user.add(request.user)

        context["RATING_CHOICES"] = Rating.RATING_CHOICES
        try:
            context["user_rating"] = Rating.objects.get(
                adventure=adventure,
                user=request.user
            ).rating
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


