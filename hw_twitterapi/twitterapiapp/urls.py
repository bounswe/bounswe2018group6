from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.main_page),

    # from the root: api/find_users/name
    path('api/find_users/<str:search_name>', views.find_users_api),

    # from the root: /find_users/name
    path('find_users/<str:search_name>', views.find_users),

    # from the root: /timegraph/api/user_id
    path('api/retweet/<str:username>', views.retweet_api),

    # from the root: /timegraph/user_id
    path('retweet/<str:username>', views.retweet),

    # API and frontend paths for 'followings' endpoint
    path('api/followings/<str:screen_name>', views.followings_api),
    path('followings/<str:screen_name>', views.followings),
]
