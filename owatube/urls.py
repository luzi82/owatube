from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'game.views.index'),
    # url(r'^owatube/', include('owatube.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^member/', include("member.urls")),
    url(r'^game/', include("game.urls") ),
    url(r'^g/(?P<game_entry>[0-9A-Za-z]+)/$', 'game.views.get_game'),
)
