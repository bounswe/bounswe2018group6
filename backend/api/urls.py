from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    path('auth/', auth_views.obtain_auth_token),
    url(r'^attendance/$', views.AttendanceCreateDestroyView.as_view()),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentView.as_view()),
    url(r'^events_list/$', views.EventListView.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventView.as_view()),
    url(r'^follow/$', views.FollowView.as_view()),
    url(r'^medias/(?P<pk>[0-9]+)/$', views.MediaView.as_view()),
    url(r'^tags/$', views.TagList.as_view()),
    url(r'^vote/$', views.VoteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# TODO user and auth endpoints:
'''
signup/
reset-password/
block/user/<int:pk>
block/event/<int:pk>
follow/user/<int:pk>/
follow/event/<int:pk>/
interest/
interest/add/<int:pk>
interest/remove/<int:pk>
'''