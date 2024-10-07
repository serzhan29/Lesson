from django.contrib import admin
from .models import Assignment, Question, Answer, StudentSubmission, StudentAnswer

# Для модели Answer (Ответов)
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Сколько пустых полей для ответов будет показано по умолчанию

# Для модели Question (Вопросов)
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Сколько пустых полей для вопросов будет показано по умолчанию
    inlines = [AnswerInline]  # Включаем ответы в вопросы

# Для модели Assignment (Задание)
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')  # Поля, которые будут отображаться в списке
    inlines = [QuestionInline]  # Включаем вопросы в задание

# Для модели StudentSubmission (Отправленные задания)
class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0  # Не добавлять пустые поля

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at')  # Показывать студента, задание и время отправки
    inlines = [StudentAnswerInline]  # Включаем ответы студента


