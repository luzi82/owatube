from django.conf.urls import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'index'),
    url(r'^(?P<game_entry>[0-9A-Za-z]+)/$', 'get_game'),
    url(r'^(?P<game_entry>[0-9A-Za-z]+)/data.txt$', 'get_game_data'),
    url(r'^(?P<game_entry>[0-9A-Za-z]+)/bgm.mp3$', 'get_game_bgm'),
    url(r'^(?P<game_entry>[0-9A-Za-z]+)/owata.swf$', 'get_game_owata'),
)
