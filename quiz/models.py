from django.db import models
from main.models import Lesson
from django.utils import timezone
from django.conf import settings

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes', default=1)
    title = models.CharField("Название теста", max_length=200)
    allow_multiple_answers = models.BooleanField("Разрешить несколько ответов", default=False)

    class Meta:
        verbose_name = "Тесттер"
        verbose_name_plural = "Тесттер"

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', default=1)
    text = models.CharField("Вопрос", max_length=500)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Тест сұрақтары"
        verbose_name_plural = "Тест сұрақтары"


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', default=1)
    text = models.CharField("Ответ", max_length=255)
    is_correct = models.BooleanField("Правильный ответ", default=False)

    def __str__(self):
        return self.text


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

    