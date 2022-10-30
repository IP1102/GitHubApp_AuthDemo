from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home),
    path('pr/', views.pr),
    path('testget/',views.testget)
    ]