from django.contrib import admin
from .models import (Quiz, Question, Answer, UserQuizResult,
                     MultyAnswer, MultyTest, TestResponse2, Tests, Points)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3  # Количество пустых полей для добавления новых ответов


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Количество пустых полей для добавления новых вопросов
    inlines = [AnswerInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson']
    inlines = [QuestionInline]  # Подключение inline для вопросов


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']
    inlines = [AnswerInline]  # Подключение inline для ответов


@admin.register(UserQuizResult)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'completed_at']


@admin.register(Points)
class PointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score']
    list_filter = ['user', 'test', 'score']


admin.site.register(MultyTest)
admin.site.register(MultyAnswer)
admin.site.register(TestResponse2)
admin.site.register(Tests)


