from django.contrib import admin
from .models import Topic, Lesson
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


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
            'short_description': CKEditorUploadingWidget ()  # Добавил для короткого описания

        }


class LessonAdmin(admin.ModelAdmin):
    form = LessonAdminForm
    list_display = ('title', 'topic', 'number', 'url')
    list_display_links = ('title', 'topic', 'number',)
    readonly_fields = ('url',)
    # Перечисляем поля, которые будут отображаться в админке в правильном формате
    fields = ('title', 'topic', 'number', 'short_description', 'description', 'video', 'photo', 'audio', 'presentation','url')

admin.site.register(Lesson, LessonAdmin)
