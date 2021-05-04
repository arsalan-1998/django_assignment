from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('collections', views.collections, name='collections'),
    path('movies/', views.create_movies, name='create_movies'),
]