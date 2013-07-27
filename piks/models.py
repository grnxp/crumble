#coding=UTF-8

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_delete
import os

# Create your models here.
class Album(models.Model):
	name = models.CharField(verbose_name='Nom', max_length=50)
	slug = models.SlugField(max_length=50, blank=False, editable=True)
	description = models.CharField(verbose_name='Description', max_length=255, null=True, blank=True)
	parent = models.ForeignKey('self', null=True, blank=True)
	created_at = models.DateTimeField(verbose_name='Date de création', auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name='Date de modification', auto_now=True)

	def __unicode__(self):
		return self.name

	def illustration(self):
		""" return an illustration for the album """
		pictures = self.picture_set.all()

		if len(pictures) > 0:
			return pictures[0].picture
		else:
			return None
	
	def parentbreadcrumb(self):
		return self.breadcrumb()[:-1]
		
	def breadcrumb(self):
		""" Returns the breadcrumb for the current album """
		if self.parent == None:
			return (self,)
		
		return self.parent.breadcrumb() + (self,)
			
	def save(self):
		""" save the album instance """
		super(Album, self).save()
		
	def path(self):
		"""
		returns the path where the album structure should be stored
		"""
		return os.sep.join((x.name for x in self.breadcrumb()))

def get_upload_path(instance, filename):
	return os.path.join('pictures', instance.album.path(), filename)
		
class Picture(models.Model):
	album = models.ForeignKey(Album)
	picture = models.ImageField(upload_to=get_upload_path)
	#picture = models.ImageField(upload_to='pictures')
	#thumbnails = models.ImageField(upload_to='thumbnails')
	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return unicode(self.picture)

# see here : https://docs.djangoproject.com/en/dev/topics/db/queries/#topics-db-queries-delete
# TODO : also delete scale and crop images.
def deleteFilesOnDisk(sender, **kwargs):
	obj = kwargs['instance']
	if os.path.exists(obj.picture.path):
		os.remove(obj.picture.path)

pre_delete.connect(deleteFilesOnDisk, sender=Picture)