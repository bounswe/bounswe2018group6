from django.urls import path
from rest_framework.authtoken import views as auth_views

from api import views

urlpatterns = [
    path('auth/', auth_views.obtain_auth_token),
]

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