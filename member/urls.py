from django.conf.urls import patterns, include, url

urlpatterns = patterns("urls.views",
    url(r'^register/$', 'register'),
)
