"""
To run all unit tests => "manage.py test"
"""

from django.test import TestCase
from piks.models import Album, Picture

class AlbumTest(TestCase):
	def setUp(self):
		"""
		inits a simple structure
		"""
		self.a1 = Album(name='album1', slug='album3')
		self.a2 = Album(name='album2', slug='album2', parent=self.a1)
		self.a3 = Album(name='album3', slug='album3', parent=self.a2)
		self.a4 = Album(name='album4', slug='album4', parent=self.a2)
		
		self.a1.save()
		self.a2.save()
		self.a3.save()
		self.a4.save()
	
	def test_Parents(self):
		self.assertTrue(self.a1.parent is None)
		self.assertTrue(self.a2.parent is self.a1)

	def test_breadcrumb(self):
		"""
		Tests that the breadcrumb is working
		"""
		
		self.assertEqual(len(self.a3.breadcrumb()), 3)
		self.assertEqual(len(self.a4.parentbreadcrumb()), 2)
		
	def test_path(self):
		"""
		Tests the path of an album (and the image_upload_to path...)
		"""
		for album in Album.objects.all():
			self.assertTrue(album.path() is not None)
			
			for crumb in album.breadcrumb():
				self.assertTrue(crumb.name in album.path())
			
		