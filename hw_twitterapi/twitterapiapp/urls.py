from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.main_page),
    # from the root: /timegraph/api/user_id
    path('api/retweet/<str:username>', views.retweet_api),

    # from the root: /timegraph/user_id
    path('retweet/<str:username>', views.retweet),

    # TODO Add two paths for each Twitter endpoint, one for the API and the other for the frontend.
]
