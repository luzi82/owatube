from django.conf.urls import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'index'),
    url(r'^list/$', 'get_game_list_fw'),
    url(r'^list/(?P<username>[0-9A-Za-z]+)/$', 'get_game_list'),
    url(r'^comment/$', 'add_game_comment'),
    url(r'^score/$', 'add_game_score'),
    url(r'^upload/$', 'add_game'),
    url(r'^edit/(?P<game_entry>[0-9A-Za-z]+)/$', 'edit_game'),
)
