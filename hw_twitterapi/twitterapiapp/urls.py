from django.urls import path

from . import views

urlpatterns = [
    # from the root: /timegraph/api/user_id
    path('api/<str:user_id>', views.timegraph_api),

    # from the root: /timegraph/user_id
    path('<str:user_id>', views.timegraph),

    # TODO Add two paths for each Twitter endpoint, one for the API and the other for the frontend.

    # API and frontend paths for 'followings' endpoint
    path('api/followings/<str:screen_name>', views.followings_api),
    path('followings/<str:screen_name>', views.followings),
]
