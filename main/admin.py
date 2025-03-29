from django.contrib import admin
from .models import Topic, Lesson, Task, URLinks
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
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
              'presentation','url', 'presentation_url', 'presentation_urls', 'video_url',
              )


admin.site.register(Lesson, LessonAdmin)


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