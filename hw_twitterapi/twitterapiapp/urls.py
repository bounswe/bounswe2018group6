from django.urls import path

from . import views

urlpatterns = [
    # from the root: /
    # main page
    path('', views.main_page),
    # from the root: api/find_users/name
    path('api/find_users/<str:search_name>', views.find_users_api),

    # from the root: /find_users/name
    path('find_users/<str:search_name>', views.find_users),
    # from the root: /api/timegraph/user_id
    path('api/timegraph/<str:user_id>', views.timegraph_api),

    # from the root: /timegraph/user_id
    path('timegraph/<str:user_id>', views.timegraph),

    # TODO Add two paths for each Twitter endpoint, one for the API and the other for the frontend.
]
