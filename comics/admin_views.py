from django.template import Context, loader
from comics.models import Comics
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext

def preview(request, comics_id):
    comics_id=int(comics_id)
    this = get_object_or_404(Comics,cid=comics_id)
    return render_to_response('admin/comics/preview.html',
                              {'comics': this},
                              RequestContext(request, {}))
                              
preview=staff_member_required(preview)


def index_thumbnail(request):
    comics_list=Comics.objects.order_by('visible')
    return render_to_response('admin/comics/index_thumbnail.html',
                              {'comics_list': comics_list})

index_thumbnail=staff_member_required(index_thumbnail)

#def code(request, comics_id):
#    comics_id=int(comics_id)
#    this = get_object_or_404(Comics,id=comics_id)
#
#    return render_to_response('admin/comics/code.html',
#                              {'comics': this},
#                              RequestContext(request, {}))


