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
        ('table', 'Таблица'),
        ('reorder', 'Перестановка'),
        # Можно добавить другие типы вопросов
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
