from piks.models import Album, Picture
from django.contrib import admin

class PictureInline(admin.StackedInline):
	model = Picture
	extra = 1

class AlbumAdmin(admin.ModelAdmin):
	# fieldsets = [
	# 	(None, { 'fields' : ['name', 'description']}),
	# ]

	inlines = [PictureInline]

	list_display = ('name', 'created_at', 'updated_at')

	list_filter = ['updated_at']

	search_fields = ['name']

	date_hierarchy = 'created_at'

	prepopulated_fields = { "slug": ("name",) }


admin.site.register(Album, AlbumAdmin)
