from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^albums/(?P<album_id>\d+)/$', 'piks.views.details'),
    url(r'^admin/piks/albums/(?P<object_id>.+)/upload_files/$', 'piks.admin_views.upload_file'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^$', 'piks.views.index'),
)

urlpatterns += staticfiles_urlpatterns()
