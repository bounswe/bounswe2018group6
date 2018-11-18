from django.urls import path

from emailer import views


urlpatterns = [
    path('activate/<slug:uidb64>/<slug:token>/', views.ActivateAccountView.as_view()),
]
