from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
]
