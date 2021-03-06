from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from website.adventure.forms import AdventureCreateForm, AdventureChangeForm, LocationForm
from website.adventure.models import Adventure, Location


@login_required
def adventure_create(request):
    if request.method == 'POST':
        form = AdventureCreateForm(request.POST, author=request.user)
        if form.is_valid():
            obj = form.save()
            messages.success(request, u"You have successfully created a new adventure.")
            return HttpResponseRedirect(reverse('location-create', args=(obj.pk,)))
    else:
        form = AdventureCreateForm(author=request.user)
    return render_to_response('adventure/adventure_form.html', {
        'create': True,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def adventure_edit(request, object_id):
    obj = get_object_or_404(Adventure, pk=object_id, author=request.user)
    if request.method == 'POST':
        form = AdventureChangeForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            messages.success(request, u"You have successfully changed the adventure.")
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form = AdventureChangeForm(instance=obj)
    return render_to_response('adventure/adventure_form.html', {
        'create': False,
        'object': obj,
        'form': form,
    }, context_instance=RequestContext(request))


@login_required
def adventure_delete(request, adventure_id):
    adventure = get_object_or_404(Adventure,
        pk=adventure_id, author=request.user)
    if request.method == 'POST':
        adventure.delete()
        messages.success(request, u"You have deleted the adventure %s" % adventure)
        return HttpResponseRedirect(reverse('adventure-list-my'))
    return render_to_response('adventure/adventure_confirm_delete.html', {
        'object': adventure,
    }, context_instance=RequestContext(request))


@login_required
def location_create(request, adventure_id):
    return location_form(request, adventure_id)


@login_required
def location_edit(request, adventure_id, location_id):
    return location_form(request, adventure_id, location_id)


@login_required
def location_delete(request, adventure_id, location_id):
    adventure = get_object_or_404(Adventure,
        pk=adventure_id, author=request.user)
    location = get_object_or_404(adventure.locations.all(), pk=location_id)
    if request.method == 'POST':
        location.delete()
        messages.success(request, u"You have deleted location %s" % location)
        return HttpResponseRedirect(
            reverse('adventure-edit', args=(adventure.pk,)))
    return render_to_response('adventure/location_confirm_delete.html', {
        'adventure': adventure,
        'object': location,
    }, context_instance=RequestContext(request))


def location_form(request, adventure_id, location_id=None):
    adventure = get_object_or_404(Adventure, pk=adventure_id, author=request.user)
    queryset = Location.objects.filter(adventure=adventure)
    if location_id is None:
        location = None
    else:
        location = get_object_or_404(queryset, pk=location_id)
    create = location is None
    if request.method == 'POST':
        form = LocationForm(request.POST, request.FILES, instance=location, adventure=adventure)
        if form.is_valid():
            location = form.save()
            if create:
                messages.success(request, u"You have successfully created the location.")
            else:
                messages.success(request, u"You have successfully changed the location.")
            if '_continue' in request.POST:
                return HttpResponseRedirect(
                    reverse('location-edit', kwargs={'adventure_id': adventure.pk, 'location_id': location.pk}))
            elif '_new' in request.POST:
                return HttpResponseRedirect(
                    reverse('location-create', kwargs={'adventure_id': adventure.pk}))
            else:
                return HttpResponseRedirect(
                    reverse('adventure-edit', args=(adventure.pk,)))
    else:
        form = LocationForm(instance=location, adventure=adventure)

    context = {
        'create': create,
        'object': location or Location(adventure=adventure),
        'form': form,
        'adventure': adventure,
    }
    return render_to_response('adventure/location_form.html', context,
        context_instance=RequestContext(request))
