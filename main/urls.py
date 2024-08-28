from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.custom_upload_file, name='custom_upload_file'),
    path('topic/<int:topic_id>/lessons', views.lesson_list_by_topic, name='lesson_list_by_topic'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('author/', views.author, name='author'),
    path('metod/', views.metod, name='metod'),
    path('books/', views.books, name='books'),
]
