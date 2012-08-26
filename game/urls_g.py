from django.conf.urls import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'index'),
    url(r'^(?P<game_entry>[0-9A-Za-z]+)/$', 'get_game'),
)
