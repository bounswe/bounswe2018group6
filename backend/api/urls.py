from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    url(r'^tags/$', views.TagList.as_view()),
    url(r'^event_medias/(?P<pk>[0-9]+)/$', views.EventMediaDetails.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetails.as_view()),
    url(r'^events/$', views.EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetails.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
