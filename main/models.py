from django.db import models
from django.utils.text import slugify
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import AbstractUser


class Topic(models.Model):
    name = models.CharField("Название урока:", max_length=200)
    photo = models.ImageField("Фото:", upload_to='photos/', blank=True, null=True)
    description = RichTextUploadingField("Описание урока", blank=True)

    class Meta:
        verbose_name = "Тақырып"
        verbose_name_plural = "Тақырып"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField("Название лекции:", max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    number = models.IntegerField("Номер лекции")
    short_description = RichTextUploadingField("Краткое описание:", blank=True)
    description = RichTextUploadingField("Полное описание:", blank=True)
    video = models.FileField("Видео:", upload_to='videos/', blank=True, null=True)
    photo = models.ImageField("Фото:", upload_to='photos/', blank=True, null=True)
    audio = models.FileField("Аудио:", upload_to='audio/', blank=True, null=True)
    presentation = models.FileField("Презентация:", upload_to='presentations/', blank=True, null=True)
    url = models.URLField("Ссылка:", max_length=200, blank=True, null=True, editable=False)

    class Meta:
        verbose_name = "Дәрістер"
        verbose_name_plural = "Дәрістер"
        unique_together = ['topic', 'number']
        ordering = ['number']

    def __str__(self):
        return f"{self.number}. {self.title}"

    def save(self, *args, **kwargs):
        if not self.url:
            slug_title = slugify(self.title)
            slug_topic = slugify(self.topic.name)
            self.url = f"/{slug_topic}/lesson-{self.number}-{slug_title}/"
        super(Lesson, self).save(*args, **kwargs)


class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    short_description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'


class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    word = models.CharField("Задание в Word:", max_length=200)
    presentation = models.CharField("Задание в PowerPoint:", max_length=200)
    url = models.URLField("Ссылка:", max_length=200, blank=True, null=True, editable=False)

    class Meta:
        verbose_name = "Қосымша материал"
        verbose_name_plural = "Қосымша материал"

    def __str__(self):
        return f"{self.lesson}. {self.url}"

    def save(self, *args, **kwargs):
        if not self.url:
            # Используем поля урока (lesson), а не несуществующий title
            slug_title = slugify(self.lesson.title)  # title теперь из lesson
            slug_topic = slugify(self.lesson.topic.name)
            self.url = f"/{slug_topic}/lesson-{self.lesson.number}-{slug_title}/"
        super(Task, self).save(*args, **kwargs)


class CustomUser(AbstractUser):
    phone_number = models.CharField("Телефонный номер: ", max_length=15, blank=True, null=True)
    photo = models.ImageField("Фото: ", upload_to='user_photos/', blank=True, null=True)
    birth_date = models.DateField("День рождение: ", blank=True, null=True)

    def __str__(self):
        return self.username
