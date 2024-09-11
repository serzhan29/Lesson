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

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', default=1)
    text = models.CharField("Сұрақ", max_length=500)
    question_type = models.CharField("Сұрақ түрі", max_length=50, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Тест сұрақтары"
        verbose_name_plural = "Тест сұрақтары"



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=1)
    text = models.CharField("Жауап", max_length=255, blank=True, null=True)
    is_correct = models.BooleanField("Дұрыс жауап", default=False)
    # Добавляем поле для ответов, требующих текстовых полей или таблиц
    filled_cells = models.JSONField("Толтырылған ұяшықтар", blank=True, null=True)
    reordered_items = models.JSONField("Қайта реттелген элементтер", blank=True, null=True)

    def __str__(self):
        return self.text if self.text else "Жауап"

    class Meta:
        verbose_name = "Жауап"
        verbose_name_plural = "Жауаптар"



class UserQuizResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.FloatField("Баллы")
    completed_at = models.DateTimeField("Дата завершения", default=timezone.now)

    class Meta:
        verbose_name = "Тест нәтижелері"
        verbose_name_plural = "Тест нәтижелері"

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"

    