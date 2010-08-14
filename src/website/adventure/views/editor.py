from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from website.adventure.forms import AdventureCreateForm


@login_required
def adventure_create(request):
    if request.method == 'POST':
        form = AdventureCreateForm(request.POST, author=request.user)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse('adventure-edit', args=(obj.pk,)))
    else:
        form = AdventureCreateForm(author=request.user)
    return render_to_response('adventure/adventure_create.html', {
        'form': form,
    }, context_instance=RequestContext(request))
