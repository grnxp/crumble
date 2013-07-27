from models import Album, Picture
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

class UploadFileForm(forms.Form):
	file = forms.FileField()

def upload_file(request, object_id):
	"""
		takes every files sent by the request upload and insert them inside the database.
	"""
	a = get_object_or_404(Album, pk=object_id)

	if request.method == 'POST':		
		for file in request.FILES.getlist('file'):
			p = Picture(picture=file, album=a)
			p.save()

		return render_to_response('success/url.html', RequestContext(request, {}))

	else:
		form = UploadFileForm()

	context = {'form':form, 'album':a }

	return render_to_response('admin/albums/upload.html', RequestContext(request, context))

# force the user to be authenticated
upload_file = staff_member_required(upload_file)