from django.db import models
from django.utils.text import slugify
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class Topic(models.Model):
    name = models.CharField("Название урока:", max_length=200)
    photo = models.ImageField("Фото:", upload_to='photos/', blank=True, null=True)
    description = RichTextUploadingField("Описание урока", blank=True)

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
    url = models.URLField("Ссылка:", max_length=200, blank=True, null=True, editable=False)

    class Meta:
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