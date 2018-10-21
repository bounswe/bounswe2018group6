from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    url(r'^comments/$', views.CommentCreate.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentDetails.as_view()),
    url(r'^event_list/$', views.EventList.as_view()),
    url(r'^events/$', views.EventCreate.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetails.as_view()),
    url(r'^medias/$', views.MediaCreate.as_view()),
    url(r'^medias/(?P<pk>[0-9]+)/$', views.MediaDetails.as_view()),
    url(r'^tags/$', views.TagList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
