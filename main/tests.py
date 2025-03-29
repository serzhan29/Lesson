from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse, resolve
from .models import Topic, Lesson, Task, CustomUser, URLinks
from .views import (CustomLoginView, register, logout_view, custom_upload_file,
                    lesson_list_by_topic, lesson_detail, profile_view, author,
                    MetodView, BooksView, ProjectView, TaskDetailView, MapView,
                    LinkListView, IncreaseClickView, topic_list)


class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Python Basics")

    def test_topic_creation(self):
        print("✅ Тест создания темы...")
        self.assertEqual(self.topic.name, "Python Basics")
        self.assertIsNotNone(self.topic.id)
        print("✅ Тема успешно создана!")


class LessonModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Python Basics")
        self.lesson = Lesson.objects.create(
            title="Introduction to Python",
            topic=self.topic,
            number=1
        )

    def test_lesson_creation(self):
        print("✅ Тест создания урока...")
        print(f"Сгенерированный URL: {self.lesson.url}")  # Вывод реального URL
        expected_url = "/python-basics/lesson-1-introduction-to-python/"
        self.assertTrue(self.lesson.url.startswith(expected_url))
        print("✅ Урок успешно создан!")

    def test_unique_lesson_number_per_topic(self):
        print("✅ Тест уникальности номера урока в теме...")
        with self.assertRaises(ValidationError):
            duplicate_lesson = Lesson(
                title="Duplicate Lesson",
                topic=self.topic,
                number=1
            )
            duplicate_lesson.full_clean()
        print("✅ Ошибка валидации успешно поймана!")


class TaskModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Python Basics")
        self.lesson = Lesson.objects.create(
            title="Introduction to Python",
            topic=self.topic,
            number=1
        )
        self.task = Task.objects.create(
            lesson=self.lesson,
            word="Write a Python script",
            presentation="Create a PowerPoint presentation on Python"
        )

    def test_task_creation(self):
        self.assertEqual(self.task.word, "Write a Python script")
        self.assertTrue(self.task.url.startswith("/python-basics/lesson-1-introduction-to-python/"))


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("securepassword123"))

    def test_user_optional_fields(self):
        self.user.phone_number = "+77001234567"
        self.user.middle_name = "Serzhanovich"
        self.user.save()
        self.assertEqual(self.user.phone_number, "+77001234567")
        self.assertEqual(self.user.middle_name, "Serzhanovich")


class URLinksModelTest(TestCase):
    def setUp(self):
        self.link = URLinks.objects.create(
            url="https://example.com",
            title="Example Website"
        )

    def test_url_creation(self):
        self.assertEqual(self.link.url, "https://example.com")
        self.assertEqual(self.link.title, "Example Website")

    def test_click_increment(self):
        self.assertEqual(self.link.clicks, 0)
        self.link.increase_clicks()
        self.assertEqual(self.link.clicks, 1)


class URLTests(TestCase):
    def test_urls_exist(self):
        print("✅ Тест доступности маршрутов...")

        url_views = {
            reverse('topic_list'): topic_list,  # Было None, теперь указываем правильное представление
            reverse('login'): CustomLoginView,
            reverse('register'): register,
            reverse('logout'): logout_view,
            reverse('custom_upload_file'): custom_upload_file,
            reverse('profile'): profile_view,
            reverse('author'): author,
            reverse('metod'): MetodView,
            reverse('books'): BooksView,
            reverse('project'): ProjectView,
            reverse('map'): MapView,
            reverse('links'): LinkListView,
        }

        for url, expected_view in url_views.items():
            resolved_view = resolve(url).func
            if hasattr(resolved_view, "view_class"):
                resolved_view = resolved_view.view_class
            print(f"Проверяем маршрут {url}...")
            self.assertEqual(resolved_view, expected_view)
            print(f"✅ {url} доступен!")

        print("✅ Все маршруты проверены успешно!")