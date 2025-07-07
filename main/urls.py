from django.urls import path
from . import views

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
    path('metod/', views.MetodView.as_view(), name='metod'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('project/', views.ProjectView.as_view(), name='project'),
    path('tasks/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('map/', views.MapView.as_view(), name='map'),
    path('links/', views.LinkListView.as_view(), name='links'),
    path('links/<int:pk>/click/', views.IncreaseClickView.as_view(), name='increase_click'),

    path('film', views.film_list, name='film_list'),
    path('film/<int:film_id>/', views.film_detail, name='film_detail'),

    path('hrono', views.TimelineEventListView.as_view(), name='hrono'),
    path('resources/', views.HistoryResourceListView.as_view(), name='list_web'),
    path('glossary/', views.glossary_list, name='glossary'),

    path('topics/', views.list_topic, name='list_topic'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),

    # add
    path('videos/', views.lesson_videos, name='lesson_videos'),
    path('iws/', views.iws, name='iws' ),
    path('textbooks/', views.textbook_list, name='textbook_list'),
    path('textbooks/<int:pk>/', views.textbook_detail, name='textbook_detail'),
]
