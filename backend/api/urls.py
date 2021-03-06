import notifications.urls
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from api import views
"""
url patterns of backend system
"""
urlpatterns = [
    url(r'^annotations/(?P<pk>[0-9]+)/$', views.AnnotationView.as_view()),
    url(r'^annotations/$', views.AnnotationView.as_view()),

    url(r'^attendance/(?P<pk>[0-9]+)/$', views.AttendanceView.as_view()),
    url(r'^attendance/$', views.AttendanceView.as_view()),

    url(r'^auth/$', views.LoginView.as_view()),

    url(r'^comments/(?P<pk>[0-9]+)/$', views.CommentView.as_view()),
    url(r'^comments/$', views.CommentView.as_view()),

    url(r'^conversations_list/$', views.ConversationListView.as_view()),
    url(r'^conversations/(?P<pk>[0-9]+)/$', views.ConversationView.as_view()),
    url(r'^conversations/$', views.ConversationView.as_view()),
    url(r'^messages/$', views.MessageView.as_view()),

    url(r'^events_list/$', views.EventListView.as_view()),
    url(r'^events_recommended_list/$', views.EventRecommendedListView.as_view()),
    url(r'^events_location/$', views.EventLocationSearchView.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventView.as_view()),
    url(r'^events/$', views.EventView.as_view()),

    url(r'^follow/(?P<pk>[0-9]+)/$', views.FollowView.as_view()),
    url(r'^follow/$', views.FollowView.as_view()),

    url(r'^medias/(?P<pk>[0-9]+)/$', views.MediaView.as_view()),
    url(r'^medias/$', views.MediaView.as_view()),

    url(r'^notifications/all/$', views.all_notifications_list),
    url(r'^notifications/unread/$', views.unread_notifications_list),
    url(r'^notifications/mark_as_read/$', views.mark_all_as_read),

    url(r'^share/(?P<pk>[0-9]+)/$', views.ShareView.as_view()),
    url(r'^share/$', views.ShareView.as_view()),

    url(r'^signup/$', views.SignUpView.as_view()),

    url(r'^tags/$', views.TagList.as_view()),

    url(r'^user/(?P<pk>[0-9]+)/$', views.UserView.as_view()),
    url(r'^users_list/$', views.UserListView.as_view()),

    url(r'^vote/(?P<pk>[0-9]+)/$', views.VoteView.as_view()),
    url(r'^vote/$', views.VoteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
