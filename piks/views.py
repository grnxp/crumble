# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from piks.models import Album, Picture
from django.core.context_processors import csrf

def default(request):
	return render_to_response('index.html', RequestContext(request, {}))

def index(request):
	print 'im heure'
	albums_list = Album.objects.all().order_by('-name')
	
	context = { 'albums_list' : albums_list }

	return render_to_response('albums/index.html', RequestContext(request, context))

def details(request, album_id):
	a = get_object_or_404(Album, pk=album_id)

	context = {'album': a}	

	return render_to_response('albums/details.html', RequestContext(request, context))

def upload_file(request, album_id):
	a = get_object_or_404(Album, pk=album_id)

	if request.method == 'POST':
		
		for file in request.FILES.getlist('file'):
			p = Picture(picture=file, album=a)
			p.save()

		return

	else:
		form = UploadFileForm()

	context = {'form':form, 'album':a }

	return render_to_response('albums/upload.html', RequestContext(request, context))