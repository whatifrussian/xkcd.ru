from django.template import RequestContext 
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response, get_object_or_404 
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from transcript.models import Transcription, UnapprovedTranscription, \
    TranscriptionForm, UnapprovedTranscriptionForm
from comics.models import Comics


def show_transcription(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    transcription = get_object_or_404(Transcription, comics=comics)
    return render_to_response('transcript/show.html',
                              {'transcription': transcription,
                               'comics': comics},
                              context_instance=RequestContext(request))

def show_form(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id) 
    if not comics.visible:
        raise Http404
    if not request.user.is_authenticated():
        if Transcription.objects.filter(comics=comics):
            return render_to_response('transcript/already_exists.html',
                                      context_instance=RequestContext(request))
        else:
            form = UnapprovedTranscriptionForm()
            return render_to_response('transcript/unapproved_form.html',
                                      {'comics': comics,
                                       'form': form},
                                      context_instance=RequestContext(request))
    else:
        try:
            instance = Transcription.objects.get(comics=comics)
            form = TranscriptionForm(instance=instance)
        except Transcription.DoesNotExist:
            form = TranscriptionForm()
        unapproved_list = UnapprovedTranscription.objects.filter(comics=comics)
        return render_to_response('transcript/edit_form.html',
                                  {'comics': comics,
                                   'unapproved_list': unapproved_list,
                                   'form': form},
                                   context_instance=RequestContext(request))

@login_required
def edit(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    instance = Transcription.objects.get_or_create(comics=comics)[0]
    form = TranscriptionForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(comics.get_absolute_url())
    else:
        unapproved_list = UnapprovedTranscription.objects.filter(comics=comics)
        return render_to_response('transcript/edit_form.html',
                                  {'comics': comics,
                                   'unapproved_list': unapproved_list,
                                   'form': form},
                                  context_instance=RequestContext(request))


# This is for not loged in user.
def add(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    if Transcription.objects.filter(comics=comics):
        return HttpResponseRedirect(reverse(show_form))
    instance = UnapprovedTranscription(comics=comics)
    form = UnapprovedTranscriptionForm(request.POST, instance=instance)
    form.comics = comics
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse(thanks, args=(comics.cid,)))
    else:
        return render_to_response('transcript/unapproved_form.html',
                                  {'comics': comics,
                                   'form': form},
                                  context_instance=RequestContext(request))

def thanks(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    return render_to_response('transcript/thanks.html',
                              {'comics': comics},
                              context_instance=RequestContext(request))

@login_required
def clear_unapproved(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    UnapprovedTranscription.objects.filter(comics=comics).delete()
    return HttpResponseRedirect(reverse(show_form, args=(comics.cid,)))
