from django.db import models
from django.utils.text import slugify
from django import forms
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import AbstractUser
from urllib.parse import urlparse, parse_qs


class Topic(models.Model):
    name = models.CharField("Сабақтың атауы:", max_length=200)
    photo = models.ImageField("Фото:", upload_to='photos/', blank=True, null=True)
    description = RichTextUploadingField("Описание урока", blank=True)

    class Meta:
        verbose_name = "Тақырып"
        verbose_name_plural = "Тақырып"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """ Лекций """
    title = models.CharField("Дәрістің атауы:", max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='lessons')
    number = models.IntegerField("Дәріс нөмірі")
    short_description = RichTextUploadingField("Қысқаша сипаттама:", blank=True)
    description = RichTextUploadingField("Толық сипаттама:", blank=True)
    video = models.FileField("Видео:", upload_to='videos/', blank=True, null=True)
    photo = models.ImageField("Фото:", upload_to='photos/', blank=True, null=True)
    audio = models.FileField("Аудио:", upload_to='audio/', blank=True, null=True)
    presentation = models.FileField("Презентация:", upload_to='presentations/', blank=True, null=True)
    url = models.URLField("Сілтеме:", max_length=200, blank=True, null=True, editable=False)
    video_url = models.URLField("Видеоға сілтеме", blank=True, null=True, default='https://www.youtube.com/embed/g-XlulPAV8E')
    presentation_url = models.CharField("Презентацияға сілтеме 1", max_length=500, blank=True, null=True,)
    presentation_urls = models.CharField("Презентацияға сілтеме 2", max_length=500,blank=True, null=True,)
    question = RichTextUploadingField("Бақылау сұрақтары:", blank=True)
    glossary = RichTextUploadingField("Глоссарий:", blank=True)

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
    question = forms.CharField(widget=CKEditorUploadingWidget())
    glossary = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'


class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    word = models.CharField("Word бағдарламасындағы тапсырма:", max_length=200)
    presentation = models.CharField("PowerPoint бағдарламасындағы тапсырма:", max_length=200)
    url = models.URLField("Сілтеме:", max_length=200, blank=True, null=True, editable=False)

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
    phone_number = models.CharField("Телефон нөмірі: ", max_length=15, blank=True, null=True)
    photo = models.ImageField("Фото: ", upload_to='user_photos/', blank=True, null=True)
    birth_date = models.DateField("Туған күн: ", blank=True, null=True)
    middle_name = models.CharField('Әкесінің аты: ', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username


class URLinks(models.Model):
    url = models.URLField(unique=True, verbose_name="Ссылка")
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
    clicks = models.PositiveIntegerField(default=0, verbose_name="Количество кликов")

    def __str__(self):
        return self.title if self.title else self.url

    def increase_clicks(self):
        """Увеличивает счетчик кликов при каждом переходе по ссылке"""
        self.clicks += 1
        self.save(update_fields=['clicks'])


class Film(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название фильма/сериала")
    description = models.TextField(verbose_name="Описание фильма/сериала")
    release_year = models.PositiveIntegerField(verbose_name="Год выпуска")
    directors = models.CharField(max_length=255, verbose_name="Режиссеры")
    video_url = models.URLField(verbose_name="Ссылка на видео")  # Ссылка на основное видео (например, трейлер или фильм)
    is_series = models.BooleanField(default=False, verbose_name="Сериал?")  # Флаг для сериалов

    def get_video_id(self):
        """
        Извлекаем ID видео из YouTube URL и возвращаем его в формате,
        подходящем для встраивания видео.
        """
        # Если ссылка на YouTube типа youtu.be/{video_id}
        if 'youtu.be' in self.video_url:
            return self.video_url.split('/')[-1].split('?')[0]  # Берем ID после последнего слэша

        # Если ссылка на YouTube типа youtube.com/watch?v={video_id}
        elif 'youtube.com' in self.video_url:
            parts = self.video_url.split('v=')
            if len(parts) > 1:
                return parts[1].split('&')[0]  # Получаем ID после v=

        # Если формат ссылки неизвестен
        return None



    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм/Сериал"
        verbose_name_plural = "Фильмы/Сериалы"


class Episode(models.Model):
    film = models.ForeignKey(Film, related_name='episodes', on_delete=models.CASCADE)  # Связь с фильмом
    episode_title = models.CharField(max_length=255, verbose_name="Название эпизода")
    video_url = models.URLField(verbose_name="Ссылка на видео")
    episode_number = models.PositiveIntegerField(verbose_name="Номер эпизода")

    def get_video_id(self):
        # Проверка на разные форматы URL YouTube
        if 'youtu.be' in self.video_url:
            return self.video_url.split('/')[-1]
        elif 'youtube.com' in self.video_url:
            parts = self.video_url.split('v=')
            if len(parts) > 1:
                return parts[1].split('&')[0]
        return None

    def __str__(self):
        return f"{self.film.title} - Эпизод {self.episode_number}"

    class Meta:
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"
        ordering = ['episode_number']
        unique_together = ['film', 'episode_number']


class TimelineEvent(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название события")
    short_description = models.CharField(max_length=500, verbose_name="Краткое описание", blank=True)
    full_description = models.TextField(verbose_name="Полное описание события", blank=True)

    # Вместо даты используем текстовое поле для времени события
    event_time = models.CharField(max_length=255, verbose_name="Время события")

    order_index = models.FloatField(verbose_name="Порядковый индекс", default=0)

    class Meta:
        ordering = ['order_index']
        verbose_name = "Событие хронологии"
        verbose_name_plural = "События хронологии"

    def __str__(self):
        return f"{self.title} ({self.event_time})"