from django.urls import path

from . import views

urlpatterns = [
    # from the root: /timegraph/api/user_id
    path('api/<str:user_id>', views.timegraph_api),

    # from the root: /timegraph/user_id
    path('<str:user_id>', views.timegraph),
]
