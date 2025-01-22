import json
from django.db import models
from main.models import Lesson
from django.utils import timezone
from django.conf import settings


class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes', default=1)
    title = models.CharField("Тест атауы", max_length=200)
    allow_multiple_answers = models.BooleanField("Бірнеше жауап беруге рұқсат етіңіз", default=False)

    class Meta:
        verbose_name = "Тесттер"
        verbose_name_plural = "Тесттер"

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Текстовое поле'),
    ]
    CHECK_TYPES = [
        ('auto', 'Автоматическая проверка'),
        ('manual', 'Ручная проверка'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', default=1)
    text = models.CharField("Сұрақ", max_length=500)
    question_type = models.CharField("Сұрақ түрі", max_length=50, choices=QUESTION_TYPES)
    check_type = models.CharField("Тип проверки", max_length=50, choices=CHECK_TYPES, default='auto')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Тест сұрақтары"
        verbose_name_plural = "Тест сұрақтары"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=1)
    text = models.CharField("Жауап", max_length=255, blank=True, null=True)
    is_correct = models.BooleanField("Дұрыс жауап", default=False)
    filled_cells = models.JSONField("Толтырылған ұяшықтар", blank=True, null=True)
    reordered_items = models.JSONField("Қайта реттелген элементтер", blank=True, null=True)

    def __str__(self):
        return self.text if self.text else "Жауап"

    class Meta:
        verbose_name = "Жауап"
        verbose_name_plural = "Жауаптар"


class UserQuizAnswer(models.Model):
    """Модель для хранения ответов студентов"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="user_answers")
    answer_text = models.TextField("Ответ студента", blank=True, null=True)  # Поле для текстового ответа
    submitted_at = models.DateTimeField("Дата отправки", auto_now_add=True)
    is_correct = models.BooleanField("Ответ верный", blank=True, null=True)  # Может быть null, если ответ проверяется вручную
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="checked_answers")
    checked_at = models.DateTimeField("Дата проверки", blank=True, null=True)  # Дата проверки преподавателем

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студентов"

    def __str__(self):
        return f"Ответ {self.user.username} на вопрос {self.question.text}"


class UserQuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField("Баллы", blank=True, null=True)  # Можно оставить пустым, пока тест не будет проверен полностью
    completed_at = models.DateTimeField("Дата завершения", default=timezone.now)

    class Meta:
        verbose_name = "Тест нәтижелері"
        verbose_name_plural = "Тест нәтижелері"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score if self.score is not None else 'Не проверен'}"



class MultyAnswer(models.Model):
    name = models.TextField("Ответ", blank=True, null=True)
    placeholder = models.CharField("Подсказка для ввода ответа",max_length=255, blank=True, null=True)

    def __str__(self):
        return f" {self.placeholder}  {self.name} "

    class Meta:
        verbose_name = "Ответ - 2"
        verbose_name_plural = "Ответы - 2"


class MultyTest(models.Model):
    name = models.CharField("Название вопроса: ", max_length=100, blank=True, null=True)
    answers = models.ManyToManyField(MultyAnswer, verbose_name="Ответы", blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='multy_tests', default=1)

    class Meta:
        verbose_name = "Вопрос - 2"
        verbose_name_plural = "Вопросы -2"

    def __str__(self):
        return f"{self.name}"


class Tests(models.Model):
    name = models.CharField("Название теста", max_length=255, blank=True, null=True)
    tests = models.ManyToManyField(MultyTest, verbose_name="Тесты", blank=True)

    def __str__(self):
        return f"Тест: {self.name}"

    class Meta:
        verbose_name = "Тест-курс - 2"
        verbose_name_plural = "Тесты-курсы - 2"


class Points(models.Model):
    """
    Модель для хранения результатов тестов пользователей.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scores", verbose_name="Пайдаланушы"
    )
    test = models.ForeignKey(
        'Tests', on_delete=models.CASCADE, related_name="scores", verbose_name="Тест"
    )
    score = models.PositiveIntegerField(verbose_name="Бағасы", help_text="Пайдаланушы тест үшін жинаған ұпайлар."
    )

    class Meta:
        verbose_name = "Бағасы"
        verbose_name_plural = "Бағасы"

    def __str__(self):
        return f"{self.user.username} - {self.test.name} - {self.score} бағасы"


class TestResponse(models.Model):
    "Не нужная модель"
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name="Тест")
    multy_test = models.ForeignKey(MultyTest, on_delete=models.CASCADE, verbose_name="Вопрос")
    selected_answers = models.ManyToManyField(MultyAnswer, verbose_name="Выбранные ответы", blank=True)
    response_text = models.TextField("Текстовый ответ", blank=True, null=True)  # Для текстовых ответов
    submitted_at = models.DateTimeField("Дата отправки", auto_now_add=True)
    response_data = models.JSONField("Ответы в формате JSON", blank=True, null=True)  # Новое поле

    class Meta:
        verbose_name = "Ответ на тест"
        verbose_name_plural = "Ответы на тесты"
        unique_together = ['student', 'test', 'multy_test']  # Уникальная комбинация студент-тест-вопрос
        indexes = [
            models.Index(fields=['student', 'test', 'multy_test']),
        ]

    def __str__(self):
        return f"{self.student} - {self.test} - {self.multy_test}"


class StudentTestResponse(models.Model):
    "Не нужная модель"
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    test = models.ForeignKey(MultyTest, on_delete=models.CASCADE, verbose_name="Тест")
    responses = models.JSONField("Ответы студента", blank=True, null=True)
    submitted_at = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Ответ студента на тест"
        verbose_name_plural = "Ответы студентов на тесты"
        # Уникальность комбинации студент + тест
        unique_together = ['student', 'test']
        # Индексы для ускорения поиска
        indexes = [
            models.Index(fields=['student', 'test']),
        ]

    def __str__(self):
        return f"{self.student} - {self.test}"


class TestResponse2(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    test = models.ForeignKey(Tests, on_delete=models.CASCADE, verbose_name="Тест")
    multy_test = models.ForeignKey(MultyTest, on_delete=models.CASCADE, verbose_name="Вопрос")
    response_data = models.JSONField("Ответы студента", blank=True, null=True)  # Сохраняем ответы как JSON
    submitted_at = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Ответ на тест -2"
        verbose_name_plural = "Ответы на тесты -2"
        unique_together = ['student', 'test', 'multy_test']  # Уникальная комбинация студент-тест-вопрос

    def __str__(self):
        return f"{self.student} - {self.test} - {self.multy_test}"

    def save(self, *args, **kwargs):
        # Сохраняем ответы в формате JSON
        if self.response_data is None:
            self.response_data = {}

        super().save(*args, **kwargs)