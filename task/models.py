from django.db import models
from django.conf import settings

class Assignment(models.Model):
    title = models.CharField(max_length=255, verbose_name="Тапсырма атауы: ")
    description = models.TextField(verbose_name="Сипаттама", blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пайдаланушы жасаған")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Құрылған күні")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тапсырма '
        verbose_name_plural = 'Тапсырмалар'


class Question(models.Model):
    TEXT = 'text'
    CHOICE = 'choice'
    MULTICHOICE = 'multichoice'

    QUESTION_TYPES = [
        (TEXT, 'Текстовое поле'),
    ]

    assignment = models.ForeignKey(Assignment, related_name='questions', on_delete=models.CASCADE, verbose_name="Тапсырма")
    question_text = models.TextField(verbose_name="Сұрақ мәтіні")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="Сұрақ түрі", default='1')
    answer_count = models.PositiveIntegerField(default=1, verbose_name="Количество ответов")  # Количество полей для ответа

    def __str__(self):
        return self.question_text

    @property
    def count_of_answers(self):
        return self.answers.count()  # Возвращает количество связанных ответов

    class Meta:
        verbose_name = 'Сұрақ '
        verbose_name_plural = 'Сұрақтар '


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name="Сұрақ")
    answer_text = models.TextField(verbose_name="Жауап")

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = 'Жауап'
        verbose_name_plural = 'Жауаптар'


class StudentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE, verbose_name="Задание")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Студент")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Оценка")
    feedback = models.TextField(blank=True, null=True, verbose_name="Комментарии к оценке")

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

    class Meta:
        unique_together = ('student', 'assignment')
        verbose_name = 'Студенттердің жауабы'
        verbose_name_plural = 'Студенттердің жауабы'


class StudentAnswer(models.Model):
    submission = models.ForeignKey(StudentSubmission, related_name='answers', on_delete=models.CASCADE, verbose_name="Студенттің жауабы")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Сұрақ")
    answer = models.TextField(verbose_name="Жауап")

    def __str__(self):
        return f"{self.submission.student.username}: {self.answer}"

    class Meta:
        verbose_name = 'Студенттердің жауабы'
        verbose_name_plural = 'Студенттердің жауаптары'
