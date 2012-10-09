from django.conf.urls import patterns, url

urlpatterns = patterns('game.views',
    url(r'^$', 'index'),
    url(r'^profile/$', 'get_user_profile'),
    url(r'^score/$', 'get_game_score_list'),
    url(r'^list/$', 'get_game_list'),
    url(r'^comment/$', 'add_game_comment'),
    url(r'^upload/$', 'add_game'),
    url(r'^submit/$', 'submit_game'),
    url(r'^edit/(?P<game_entry>[0-9A-Za-z]+)/$', 'edit_game'),
    url(r'^edit/(?P<game_entry>[0-9A-Za-z]+)/data.txt$', 'get_game_data'),
    url(r'^edit/(?P<game_entry>[0-9A-Za-z]+)/bgm.mp3$',  'get_game_bgm'),
)
