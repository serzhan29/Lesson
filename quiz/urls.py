from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),

    path('test/success/', views.test_success, name='test_success'),

    path('tests/', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),

    path('responses/', views.all_student_responses, name='all_student_responses'),
    path('responses/<int:response_id>/', views.student_response_detail, name='student_response_detail'),
    path('responses/test/<int:test_id>/', views.student_response_detail, name='student_response_detail_by_test'),

    path('all-student-responses/', views.all_student_responses, name='student_responses'),
    path('add-or-update-score/', views.add_or_update_score, name='add_or_update_score'),
]

