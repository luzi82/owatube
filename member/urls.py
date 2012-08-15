from django.conf.urls import patterns, url

urlpatterns = patterns("member.views",
    url(r'^register/$', 'register'),
    url(r'^register_success/$', 'register_success'),
)

urlpatterns += patterns("django.contrib.auth.views",
    url(r'^login/$', 'login', {'template_name': 'login.tmpl'}),
    url(r'^logout/$', 'logout', {'template_name': 'logout.tmpl'}),
)
