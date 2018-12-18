from django.urls import path

from emailer import views


urlpatterns = [
    path('activate/<int:uid>/<slug:token>/', views.ActivateAccountView.as_view()),
]
