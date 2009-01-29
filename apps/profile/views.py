from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from profile.models import ProfileForm, Profile

@login_required
def edit(request):
    try:
        profile = request.user.get_profile()
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(edit) + '?saved')
    else:
        form = ProfileForm(instance=profile)

    return render_to_response('profile/edit.html',
                              {'form': form,
                               'saved': True if request.GET.has_key('saved')\
                                   else False},
                              context_instance = RequestContext(request))

