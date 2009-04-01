from django.template import RequestContext
from django.shortcuts import render_to_response

from comics.models import Comics
from django.contrib.auth.models import User
from profile.models import Profile
from livejournal.models import Post
from transcript.models import UnapprovedTranscription


def show(request):
    stat = {}
    stat['comics'] = Comics.objects.count()
    stat['unpublished'] = Comics.objects.filter(visible=False).count()
    stat['ready'] = Comics.objects.filter(visible=False, ready=True).count()
    stat['lj'] = Post.objects.count()
    stat['transcriptions'] = Comics.objects.exclude(transcription='').count()
    stat['unapproved_transcriptions'] = UnapprovedTranscription.objects.count()
    stat['authors'] = User.objects.count()
    stat['superusers'] = User.objects.filter(is_staff=True).count()
    return render_to_response('statistics/show.html',
                              stat,
                              context_instance=RequestContext(request))

