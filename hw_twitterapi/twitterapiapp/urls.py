from django.urls import path

from . import views

urlpatterns = [
    # from the root: api/find_users/name
    path('api/find_users/<str:search_name>', views.find_users_api),

    # from the root: /find_users/name
    path('find_users/<str:search_name>', views.find_users),
]
