import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Topic, Lesson, Task, CustomUser, URLinks
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from .forms import UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView, View


class CustomLoginView(LoginView):
    template_name = 'main/registration/login.html'
    success_url = reverse_lazy('topic_list')  # Измените на URL, куда нужно перенаправить после входа


# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/registration/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('topic_list')


@csrf_exempt
def custom_upload_file(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        try:
            uploaded_file = request.FILES['upload']
            file_name = uploaded_file.name
            file_path = os.path.join('photos', file_name)  # Путь к файлу внутри папки photo

            # Сохранение файла в папку media/photo
            file_save_path = os.path.join(settings.MEDIA_ROOT, file_path)
            os.makedirs(os.path.dirname(file_save_path), exist_ok=True)  # Создаем директорию, если она не существует

            with default_storage.open(file_save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_url = os.path.join(settings.MEDIA_URL, file_path)
            return JsonResponse({'message': 'File uploaded successfully!', 'url': file_url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def topic_list(request):
    topics = Topic.objects.all()
    return render(request, 'main/page/topic_list.html', {'topics': topics})


def lesson_list_by_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    lessons = topic.lessons.all()
    return render(request, 'main/page/lessons.html', {'topic': topic, 'lessons': lessons})


@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Получаем все задания, связанные с конкретной лекцией
    task = Task.objects.filter(lesson=lesson).first()  # Если одно задание, используем first()
    related_lessons = Lesson.objects.filter(topic=lesson.topic).exclude(id=lesson_id)
    quizzes = lesson.quizzes.all()  # Получаем тесты, связанные с этой лекцией

    return render(request, 'main/page/detail_lesson.html', {
        'lesson': lesson,
        'list': related_lessons,
        'quizzes': quizzes,  # Передаем связанные тесты
        'task': task,  # Передаем task, связанный с этой лекцией
    })



@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)  # Обрабатывайте файлы
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля после сохранения
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'user': request.user,
        'form': form
    }
    return render(request, 'main/info/profile.html', context)

def author(request):
    user = get_object_or_404(CustomUser, id=1)
    return render(request, 'main/info/author.html',{
        'user':user,
    })


class BooksView(TemplateView):
    """ Представление для страницы книг """
    template_name = 'main/info/books.html'


class MetodView(TemplateView):
    """ Представление для страницы методических материалов """
    template_name = 'main/info/metod.html'


class ProjectView(TemplateView):
    """ Представление для страницы проектов """
    template_name = 'main/info/project.html'

class TaskDetailView(LoginRequiredMixin, DetailView):
    """ Представление для отображения деталей задания """
    model = Task
    template_name = 'main/info/word.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return get_object_or_404(Task, id=self.kwargs.get('task_id'))


class MapView(TemplateView):
    """ Карта """
    template_name = 'main/info/map.html'


class LinkListView(ListView):
    """ Ссылки на тесты """
    model = URLinks
    template_name = 'main/info/link_list.html'
    context_object_name = 'links'
    ordering = ['id']  # Сортировка по ID


class IncreaseClickView(View):
    """ Увеличивает количество кликов по ссылке """
    def post(self, request, pk, *args, **kwargs):
        link = get_object_or_404(URLinks, id=pk)
        link.increase_clicks()
        return JsonResponse({'status': 'success', 'clicks': link.clicks})

