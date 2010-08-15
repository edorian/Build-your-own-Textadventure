from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def profile(request):
    profile = request.user.profile
    return render_to_response('profile/profile_detail.html', {
        'object': profile,
        'adventures_completed': request.user.completed_adventure.count(),
        'adventures_started': request.user.started_adventure.count(),
    }, context_instance=RequestContext(request))
