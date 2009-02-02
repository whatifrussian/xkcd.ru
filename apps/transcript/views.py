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
                              {'comics': comics},
                              context_instance=RequestContext(request))

def show_form(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id) 
    if not comics.visible:
        raise Http404
    if not request.user.is_authenticated():
        try:
            comics.transcription
            return render_to_response('transcript/already_exists.html',
                                      context_instance=RequestContext(request))
        except Transcription.DoesNotExist:
            form = UnapprovedTranscriptionForm()
            return render_to_response('transcript/unapproved_form.html',
                                      {'comics': comics,
                                       'form': form},
                                      context_instance=RequestContext(request))
    else:
        try:
            form = TranscriptionForm(instance=comics.transcription)
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
        UnapprovedTranscription.objects.filter(comics=comics).delete()
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
    try:
        comics.transcription
        return HttpResponseRedirect(reverse(show_form, args=(comics.cid,)))
    except Transcription.DoesNotExist:
        pass
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

@login_required
def list_unapproved(request):
    unapproved_list = UnapprovedTranscription.objects.all()
    comics_map = {}
    for transcription in unapproved_list:
        comics = transcription.comics
        if comics_map.has_key(comics.cid):
            comics_map[comics.cid][1]+=1
        else:
            comics_map[comics.cid]=[comics, 1]
    comics_list = []
    for i in comics_map:
        comics_list.append(comics_map[i][0])
        comics_list[-1].repeats = comics_map[i][1]
    return render_to_response('transcript/list.html',
                              {'comics_list': comics_list},
                              context_instance=RequestContext(request))
