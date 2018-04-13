from django.urls import path

from . import views

urlpatterns = [
    # from the root: /
    # main page
    path('', views.main_page),

    # from the root: /api/trends-by-place/WOEID
    path('api/trends-by-place/<int:WOEID>', views.trends_by_place_api),

    # from the root: /trends-by-place/WOEID
    path('trends-by-place/<int:WOEID>', views.trends_by_place),

    # TODO Add two paths for each Twitter endpoint, one for the API and the other for the frontend.
]
