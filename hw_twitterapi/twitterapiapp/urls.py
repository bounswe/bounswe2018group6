from django.urls import path

from . import views

urlpatterns = [
    # from the root: api/friends/user_id
    path ( 'api/find_friends/<str:user_id>', views.find_friends_api ),

    # from the root: /find_friends/user_id
    path ( 'find_friends/<str:user_id>', views.find_friends ),

