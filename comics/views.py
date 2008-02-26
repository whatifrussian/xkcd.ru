from django.template import Context, loader
from comics.models import Comics
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
#from django.contrib.sites.models import Site


# Create your views here.
def index(request):
    class NoComics:
	def __init__(self,id):
	    self.id=id
	fake=True
    br=20
    tmp_comics_list = Comics.objects.filter(visible=True).order_by('id')
    last_id= Comics.objects.filter(visible=True).order_by('-id')[0].id
    comics_list=[NoComics(i) for i in xrange(1,last_id+1)]
    for comics in tmp_comics_list:
	comics_list[comics.id-1]=comics
    for i in xrange(br-1,len(comics_list),br):
	comics_list[i].br=True
    return render_to_response('comics/index.html',
                              {'comics_list': comics_list})


def index_thumbnail(request):
    comics_list=Comics.objects.filter(visible=True).order_by('-pub_date')
    return render_to_response('comics/index_thumbnail.html',
                              {'comics_list': comics_list})

def detail(request, comics_id):
    comics_id=int(comics_id)
    this = get_object_or_404(Comics,id=comics_id,visible=True)
    first = Comics.objects.filter(visible=True).order_by('id')[0]
    last = Comics.objects.filter(visible=True).order_by('-id')[0]
    try:
        prev = Comics.objects.filter(visible=True,id__lt=comics_id).order_by('-id')[0]
    except IndexError:
        prev = None
    try:
        next = Comics.objects.filter(visible=True,id__gt=comics_id).order_by('id')[0]
    except IndexError:
        next = None

    random = reverse('comics.views.random', args=(comics_id,))

    return render_to_response('comics/detail.html',
                              {'comics': this,
                               'first': first,
                               'last': last,
                               'prev': prev,
                               'next': next,
                               'random': random})

def detail_unpublished(request, comics_id, timestamp):
    comics_id=int(comics_id)
    this = get_object_or_404(Comics,visible=False,id=comics_id)
    if this.pub_date.strftime('%s')!=timestamp:
        raise Http404

    return render_to_response('comics/detail_unpublished.html',
                              {'comics': this})

def random(request,comics_id=-1):
    try:
        random = Comics.objects.filter(visible=True).exclude(id=comics_id).order_by('?')[0]
        return HttpResponseRedirect(random.get_absolute_url())
    except IndexError:
        raise Http404


def code(request, comics_id):
    comics_id=int(comics_id)
    this = get_object_or_404(Comics,visible=True,id=comics_id)

    return render_to_response('comics/code.html',
                              {'comics': this})

