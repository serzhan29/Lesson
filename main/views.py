import os
import uuid
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Topic, Lesson, Task, CustomUser, URLinks, Film
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
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
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator


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


# Допустимые расширения файлов
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@csrf_protect  # Включаем CSRF-защиту
def custom_upload_file(request):
    if request.method != 'POST' or 'upload' not in request.FILES:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        uploaded_file = request.FILES['upload']
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()

        # Проверка расширения файла
        if file_ext not in ALLOWED_EXTENSIONS:
            raise SuspiciousOperation("Недопустимый формат файла")

        # Проверка размера файла
        if uploaded_file.size > MAX_FILE_SIZE:
            raise SuspiciousOperation("Файл слишком большой (макс. 10MB)")

        # Генерация безопасного имени файла
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join('photos', unique_filename)
        file_save_path = os.path.join(settings.MEDIA_ROOT, file_path)

        # Создание папки, если она не существует
        os.makedirs(os.path.dirname(file_save_path), exist_ok=True)

        # Сохранение файла
        with default_storage.open(file_save_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        file_url = os.path.join(settings.MEDIA_URL, file_path)

        return JsonResponse({'message': 'Файл успешно загружен!', 'url': file_url})

    except SuspiciousOperation as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Ошибка сервера'}, status=500)


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
    task = Task.objects.filter(lesson=lesson).first()
    related_lessons = Lesson.objects.filter(topic=lesson.topic).exclude(id=lesson_id)
    quizzes = lesson.quizzes.all()

    return render(request, 'main/page/detail_lesson.html', {
        'lesson': lesson,
        'list': related_lessons,
        'quizzes': quizzes,
        'task': task,
        'presentation': lesson.presentation,  # Передаём презентацию
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

def film_list(request):
    """Отображение списка фильмов и сериалов с пагинацией и фильтрами"""
    films = Film.objects.all()

    # Фильтрация
    year = request.GET.get('year')
    director = request.GET.get('director')

    # Проверка на корректные значения
    if year and year != 'None':
        try:
            films = films.filter(release_year=int(year))
        except ValueError:
            pass  # если год некорректный, не фильтруем по нему

    if director and director != 'None':
        films = films.filter(directors__icontains=director)

    # Пагинация
    paginator = Paginator(films, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Уникальные значения для фильтра
    all_years = Film.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    all_directors = Film.objects.values_list('directors', flat=True).distinct().order_by('directors')

    context = {
        'page_obj': page_obj,
        'all_years': all_years,
        'all_directors': all_directors,
        'selected_year': year if year != 'None' else '',
        'selected_director': director if director != 'None' else '',
    }

    return render(request, 'main/info/film_list.html', context)


def film_detail(request, film_id):
    film = get_object_or_404(Film, id=film_id)

    # Извлекаем ID видео из YouTube URL, если видео с YouTube
    if 'youtube.com' in film.video_url or 'youtu.be' in film.video_url:
        video_id = film.video_url.split('v=')[-1].split('&')[0]  # Извлекаем ID
    else:
        video_id = None

    return render(request, 'main/info/film_detail.html', {'film': film, 'video_id': video_id})