from django.conf.urls import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'index'),
    url(r'^profile/$', 'get_user_profile'),
    url(r'^score/$', 'get_game_score_list'),
    url(r'^list/$', 'get_game_list'),
    url(r'^comment/$', 'add_game_comment'),
    url(r'^add_score/$', 'add_game_score'),
    url(r'^upload/$', 'add_game'),
    url(r'^edit/(?P<game_entry>[0-9A-Za-z]+)/$', 'edit_game'),
)
