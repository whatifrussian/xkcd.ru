# *- coding: utf-8 *-
from datetime import datetime

import lj

from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.contrib.sitemaps import ping_google
from django.conf import settings

from comics.models import Comics, ComicsForm
from profile.models import Profile
from livejournal.models import Post
from transcript.models import UnapprovedTranscription


class NoComics:
    def __init__(self, cid):
        self.cid = cid
        self.fake = True

    def get_absolute_url(self):
        return 'http://xkcd.com/%d/' % self.cid


def last(request):
    try:
        last_comics = Comics.objects.filter(visible=True).order_by('-published')[0]
    except IndexError:
        return HttpResponseRedirect(reverse(index_numbers))
    if request.GET.has_key('json'):
        return HttpResponseRedirect(last_comics.get_absolute_url() + '?json')
    else:
        return HttpResponseRedirect(last_comics.get_absolute_url())


def index_numbers(request): 
    try:
        if request.user.is_authenticated():
            tmp_comics_list = Comics.objects.order_by('cid')
            last_id = Comics.objects.order_by('-cid')[0].cid
        else:
            tmp_comics_list = Comics.objects.filter(visible=True).order_by('cid')
            last_id = Comics.objects.filter(visible=True).order_by('-cid')[0].cid
        comics_list=[NoComics(i) for i in xrange(1, last_id + 1)]
        for comics in tmp_comics_list:
            comics_list[comics.cid - 1] = comics
    except IndexError:
        comics_list = None
    return render_to_response('comics/index_numbers.html',
                              {'comics_list': comics_list},
                              context_instance=RequestContext(request))


def index_thumbnail(request):
    if request.user.is_authenticated():
        comics_list = Comics.objects.order_by('-cid')
    else:
        comics_list = Comics.objects.filter(visible=True).order_by('-cid')
    return render_to_response('comics/index_thumbnail.html',
                              {'comics_list': comics_list},
                              context_instance=RequestContext(request))

def detail(request, comics_id):
    comics_id = int(comics_id)
    this = get_object_or_404(Comics, cid=comics_id)
    if not this.visible:
        if request.user.is_authenticated():
           return HttpResponseRedirect(this.get_absolute_url())
        else:
            raise Http404
    # Do we need this? 
    if request.POST.has_key('code'):
        return HttpResponseRedirect(this.get_absolute_url() + '?code')
    if request.POST.has_key('show_transcription'):
        return HttpResponseRedirect(this.get_absolute_url() + '?transcription')
    if request.POST.has_key('hide_transcription'):
        return HttpResponseRedirect(this.get_absolute_url())
    if request.GET.has_key('transcription'):
        show_transcription = True
    else:
        show_transcription = False

    # Get transcription.
    unapproved = UnapprovedTranscription.objects.filter(comics=this).\
        count()
    lj_post = None
    if request.user.is_staff:
        try:
            lj_post = Post.objects.get(comics=this)
        except Post.DoesNotExist:
            pass
    first = Comics.objects.filter(visible=True).order_by('cid')[0]
    last = Comics.objects.filter(visible=True).order_by('-cid')[0]
    try:
        prev = Comics.objects.filter(visible=True,cid__lt=comics_id).\
            order_by('-cid')[0]
    except IndexError:
        prev = None
    try:
        next = Comics.objects.filter(visible=True,cid__gt=comics_id).\
            order_by('cid')[0]
    except IndexError:
        next = None

    random = reverse('comics.views.random', args=(comics_id, ))

    if request.GET.has_key('json'):
        return render_to_response('comics/api/detail.html',
                                  {'comics': this,
                                   'first': first,
                                   'last': last,
                                   'prev': prev,
                                   'next': next,
                                   'random': random,
                                   'host': request.META['HTTP_HOST'],
                                   },
                                  context_instance=RequestContext(request),
                                  mimetype='application/json')
    else:
        return render_to_response('comics/detail.html',
                                  {'comics': this,
                                   'first': first,
                                   'last': last,
                                   'prev': prev,
                                   'next': next,
                                   'code': True if request.GET.has_key('code')\
                                       else False,
                                   'show_transcription': show_transcription,
                                   'random': random,
                                   'lj': request.GET['lj'] if \
                                       request.GET.has_key('lj') \
                                       else False,
                                   'msg': request.GET['msg'] if \
                                       request.GET.has_key('msg') \
                                       else False,
                                   'unapproved': unapproved,
                                   'lj_post': lj_post},
                                  context_instance=RequestContext(request))


def detail_unpublished(request, comics_id, timestamp):
    comics_id = int(comics_id)
    this = get_object_or_404(Comics, cid=comics_id)
    if this.visible:
        return HttpResponseRedirect(this.get_absolute_url())
    if request.user.is_staff:
        if request.POST.has_key('no'):
            return HttpResponseRedirect(this.get_absolute_url())
        elif request.POST.has_key('publish'):
            return HttpResponseRedirect(this.get_absolute_url() + '?publish')
    if this.created.strftime('%s') != timestamp:
        raise Http404
    mail_set = this.mail_set.all().order_by('date')
    return render_to_response('comics/detail_unpublished.html',
                              {'comics': this,
                               'mail_set': mail_set,
                               'publish': True if \
                                   request.GET.has_key('publish') \
                                   else False},
                              context_instance=RequestContext(request))

def random(request,comics_id = -1):
    try:
        random = Comics.objects.filter(visible=True).exclude(cid=comics_id).\
            order_by('?')[0]
        if request.GET.has_key('json'):
            return HttpResponseRedirect(random.get_absolute_url() + '?json')
        else:
            return HttpResponseRedirect(random.get_absolute_url())
    except IndexError:
        raise Http404


#Auth users methods

@login_required
def index_unpublished(request):
    comics_list = Comics.objects.filter(visible=False).\
        order_by('reviewed','-ready','created')
    return render_to_response('comics/index_unpublished.html',
                              {'comics_list': comics_list},
                              context_instance=RequestContext(request))
    
@login_required
def edit(request, comics_id):
    comics_id = int(comics_id)
    this = get_object_or_404(Comics, cid=comics_id)
    if request.user != this.author:
        raise Http404
    elif request.POST.has_key('edit'):
        return HttpResponseRedirect(reverse(edit, args=(this.cid, )) + '#edit')
    elif request.method == 'POST':
        form = ComicsForm(request.POST, request.FILES, instance=this)
        try:
            if form.is_valid():
                this.reviewed = False
                this.ready = False
                this = form.save()
                if not request.POST.has_key('continue'):
                    return HttpResponseRedirect(this.get_absolute_url())
        except IntegrityError:
            form.errors['cid'] = ['Этот перевод уже есть']

    else:
        form = ComicsForm(instance=this)
    return render_to_response('comics/edit_form.html',
                              {'comics': this,
                               'edit': True,
                               'form': form},
                              context_instance = RequestContext(request))

@login_required
def add(request):
    if request.method == 'POST':
        if request.POST.has_key('cancel'):
            return HttpResponseRedirect(reverse(index_unpublished))
        this = Comics(author=request.user)
        form = ComicsForm(request.POST, request.FILES, instance=this)
        try:
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(index_unpublished))
        except IntegrityError:
            form.errors['cid'] = ['Этот перевод уже есть.']
    else:            
        form = ComicsForm()
    return render_to_response('comics/edit_form.html',
                              {'form': form},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff)
def publish(request, comics_id):
    comics_id = int(comics_id)
    this = get_object_or_404(Comics, cid=comics_id, visible=False)
    this.visible = True
    this.published = datetime.now()
    this.save()
    if settings.PING_GOOGLE:
        try:
            ping_google()
        except:
            pass
    if request.POST.has_key('lj'):
        return HttpResponseRedirect(reverse('livejournal.views.post', args=(comics_id, )))
    return HttpResponseRedirect(this.get_absolute_url())

@user_passes_test(lambda u: u.is_staff)
def review(request, comics_id):
    comics_id = int(comics_id)
    this = get_object_or_404(Comics, cid=comics_id)
    if request.POST.has_key('ready'):
        this.ready = True
    else:
        this.ready = False
    this.reviewed = True
    this.save()
    return HttpResponseRedirect(reverse(index_unpublished))
