from django.contrib import admin
from openpyxl.styles.builtins import title

from .models import (Topic, Lesson, Task, URLinks, Film, CustomUser,
                     Episode, TimelineEvent, HistoryResource, GlossaryTerm, TaskName, TopicName, IWS, Textbook)
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class LessonAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget ())

    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'description': CKEditorUploadingWidget (),
            'short_description': CKEditorUploadingWidget (),
            'question': CKEditorUploadingWidget (),
            'glossary': CKEditorUploadingWidget (),

        }


class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('title', 'topic', 'number', 'url')
    list_display_links = ('title', 'topic', 'number',)
    readonly_fields = ('url',)
    # Перечисляем поля, которые будут отображаться в админке в правильном формате
    fields = ('title', 'topic', 'number', 'short_description', 'description', 'question','glossary', 'video',
              'photo', 'audio',
              'presentation','url', 'presentation_url', 'presentation_urls',
              'video_url', 'video_2', 'video_3', 'video_4', 'video_5'
              )

admin.site.register(Lesson, LessonAdmin)


class TextbookAdminForm(forms.ModelForm):
    class Meta:
        model = Textbook
        fields = '__all__'
        widgets = {
            'description': CKEditorUploadingWidget(),
        }


@admin.register(Textbook)
class TextbookAdmin(admin.ModelAdmin):
    form = TextbookAdminForm
    list_display = ['name', 'lesson']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'url')
    list_display_links = ('id', 'lesson', 'url')


admin.site.register(Task, TaskAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'get_groups')
    list_display_links = ('id', 'username', 'first_name', 'last_name',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'),
         {'fields': ('first_name', 'last_name', 'middle_name', 'email', 'phone_number', 'photo', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()]) if obj.groups.exists() else "Нет группы"

    get_groups.short_description = 'Құқықтар'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone_number', 'photo', 'birth_date'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(URLinks)
class URLinksAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'clicks')
    search_fields = ('url', 'title')
    list_filter = ('title',)
    readonly_fields = ('clicks',)  # Эти поля нельзя редактировать вручную


class EpisodeInline(admin.TabularInline):
    model = Episode
    extra = 1  # Добавляем одну пустую строку для создания нового эпизода
    fields = ('episode_number', 'episode_title', 'video_url')  # Поля для редактирования эпизодов
    # readonly_fields = ('episode_number',)  # Если нужно сделать номер эпизода только для чтения
    ordering = ('episode_number',)  # Сортировка эпизодов по номеру

class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'directors', 'is_series', 'video_url', 'get_episode_count')
    list_filter = ('release_year', 'is_series')  # Фильтрация по году и сериалам
    search_fields = ('title', 'directors')  # Поиск по названию и режиссерам
    list_editable = ('video_url',)
    fields = ('title', 'description', 'release_year', 'directors', 'is_series', 'video_url')
    ordering = ('release_year',)
    inlines = [EpisodeInline]  # Включаем редактирование эпизодов внутри фильма

    def get_episode_count(self, obj):
        """Метод для отображения количества эпизодов в фильме"""
        return obj.episodes.count()
    get_episode_count.short_description = 'Кол-во эпизодов'  # Название колонки в списке

admin.site.register(Film, FilmAdmin)
admin.site.register(Episode)


@admin.register(TimelineEvent)
class TimelineEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_time', 'order_index', 'short_description')
    search_fields = ('title', 'short_description', 'full_description')
    list_filter = ('event_time',)
    ordering = ('order_index',)


@admin.register(HistoryResource)
class HistoryResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'url', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('resource_type', 'created_at')


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ('title' , 'category')
    list_display_links = ('title', 'category')



# Инлайн-редактирование заданий внутри темы
class TaskInline(admin.TabularInline):
    model = TaskName
    extra = 1  # сколько пустых форм показывать по умолчанию
    fields = ['number', 'title', 'description', 'image']  # какие поля показывать
    show_change_link = True

# Админка для тем
@admin.register(TopicName)
class TopicNameAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [TaskInline]

# Отдельная админка для заданий (на всякий случай)
@admin.register(TaskName)
class TaskNameAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'topic']
    list_filter = ['topic']


@admin.register(IWS)
class IWSAdmin(admin.ModelAdmin):
    list_display = ['number', 'name']
    list_display_links = ['number', 'name']