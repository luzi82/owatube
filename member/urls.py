from django.conf.urls import patterns, url

urlpatterns = patterns("member.views",
    url(r'^register/$', 'register'),
    url(r'^register_success/$', 'register_success'),
)
