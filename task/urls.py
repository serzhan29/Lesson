from django.urls import path
from . import views

urlpatterns = [
    path('assignments/', views.assignment_list, name='assignment_list'),  # Список всех тестов
    path('assignments/<int:assignment_id>/', views.assignment_view, name='assignment_detail'),  # Просмотр теста и сдача
]
