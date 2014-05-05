from django.template import RequestContext 
from django.core.urlresolvers import reverse 
from django.shortcuts import render_to_response, get_object_or_404 
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from transcript.models import UnapprovedTranscription,\
    UnapprovedTranscriptionForm
from comics.models import Comics, TranscriptionForm
from comics.views import last


def show_form(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id) 
    if not comics.visible:
        raise Http404
    if not request.user.is_authenticated():
        if comics.transcription:
            return render_to_response('transcript/already_exists.html',
                                      context_instance=RequestContext(request))
        else:
            form = UnapprovedTranscriptionForm()
            return render_to_response('transcript/unapproved_form.html',
                                      {'comics': comics,
                                       'form': form},
                                      context_instance=RequestContext(request))
    else:
        form = TranscriptionForm(instance=comics)
        form.transcription = comics.transcription
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
    form = TranscriptionForm(request.POST, instance=comics)
    if form.is_valid():
        # Don't update on no edit.
        if form.cleaned_data['transcription'] != comics.transcription:
            form.save()
            UnapprovedTranscription.objects.filter(comics=comics).delete()
        if 'next' in request.POST:
            return HttpResponseRedirect(reverse(random, args=(comics_id,)))
        else:
            return HttpResponseRedirect(comics.get_absolute_url())
    else:
        unapproved_list = UnapprovedTranscription.objects.filter(comics=comics)
        return render_to_response('transcript/edit_form.html',
                                  {'comics': comics,
                                   'unapproved_list': unapproved_list,
                                   'form': form},
                                  context_instance=RequestContext(request))

def random(request, comics_id=None):
    try:
        if comics_id is None:
            comics = Comics.objects.filter(visible=True, transcription='')\
                .order_by('?')[0]
        else:
            comics = Comics.objects.exclude(cid=comics_id)\
                .filter(visible=True, transcription='')\
                .order_by('?')[0]
        return HttpResponseRedirect(reverse(show_form, args=(comics.cid,)))
    except IndexError:
        return HttpResponseRedirect(reverse(last))

# This is for not loged in user.
def add(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    if comics.transcription:
        return HttpResponseRedirect(reverse(show_form, args=(comics.cid,)))
    instance = UnapprovedTranscription(comics=comics)
    form = UnapprovedTranscriptionForm(request.POST, instance=instance)
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
    untranscribed = len(Comics.objects.filter(visible=True, transcription='')\
                            .exclude(cid=comics_id))
    return render_to_response('transcript/thanks.html',
                              {'comics': comics,
                               'untranscribed': untranscribed},
                              context_instance=RequestContext(request))

@login_required
def clear_unapproved(request, comics_id):
    comics_id = int(comics_id)
    comics = get_object_or_404(Comics, cid=comics_id, visible=True)
    UnapprovedTranscription.objects.filter(comics=comics).delete()
    return HttpResponseRedirect(reverse(show_form, args=(comics.cid,)))

@login_required
def list_unapproved(request):
    # TODO: on update to Django 1.1 change this using aggergation functions.
    unapproved_list = UnapprovedTranscription.objects.all()
    comics_map = {}
    for transcription in unapproved_list:
        comics = transcription.comics
        if comics.cid in comics_map:
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
