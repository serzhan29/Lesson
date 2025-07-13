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
    video_url = models.URLField("Видеоға сілтеме - 1", blank=True, null=True, default='https://www.youtube.com/embed/')
    video_2 = models.URLField("Видеоға сілтеме - 2 ", blank=True, null=True,)
    video_3 = models.URLField("Видеоға сілтеме - 3", blank=True, null=True,)
    video_4 = models.URLField("Видеоға сілтеме - 4", blank=True, null=True,)
    video_5 = models.URLField("Видеоға сілтеме - 5", blank=True, null=True,)
    presentation_url = models.CharField("Презентацияға сілтеме 1", max_length=500, blank=True, null=True,)
    presentation_urls = models.CharField("Презентацияға сілтеме 2", max_length=500,blank=True, null=True,)
    presentation_url3 = models.CharField("Презентацияға сілтеме - 3 ", blank=True, null=True, max_length=500)
    presentation_url4 = models.CharField("Презентацияға сілтеме - 4 ", blank=True, null=True, max_length=500)
    presentation_url5 = models.CharField("Презентацияға сілтеме - 5 ", blank=True, null=True, max_length=500)
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


class Textbook(models.Model):
    name = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='textbooks')
    description = RichTextUploadingField("Толық сипаттама:", blank=True)


    def __str__(self):
        return f"{self.lesson.title}. {self.name}"


    class Meta:
        verbose_name = 'Хрестоматия'
        verbose_name_plural = 'Хрестоматия'

class LessonForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    short_description = forms.CharField(widget=CKEditorUploadingWidget())
    question = forms.CharField(widget=CKEditorUploadingWidget())
    glossary = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'


class TextbookForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Textbook
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

    class Meta:
        verbose_name = 'Kahoot тест'
        verbose_name_plural = 'Kahoot тесттер'


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
    """ Хронология """
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


class HistoryResource(models.Model):
    """ Полезные сайты для изучения историй Казахстана """
    RESOURCE_TYPE_CHOICES = [
        ('website', 'Интернет-сайт'),
        ('virtual_tour', 'Виртуальный тур'),
        ('3D', '3Д видеотур иесі'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    url = models.URLField(verbose_name="Ссылка")
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES, verbose_name="Тип ресурса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '3D Видеотур'
        verbose_name_plural = '3D Видеотурлар'


class GlossaryTerm(models.Model):
    """ Глоссарий """
    title = models.CharField("Термин", max_length=200, unique=True)
    definition = models.TextField("Определение")
    category = models.CharField("Категория", max_length=100, blank=True)


    class Meta:
        verbose_name = "Термин глоссария"
        verbose_name_plural = "Глоссарий"
        ordering = ['title']

    def __str__(self):
        return self.title


# Модель Темы
class TopicName(models.Model):
    title = models.CharField("Название темы", max_length=255)
    url = models.URLField('Ссылка', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'БӨЖ тест'
        verbose_name_plural = 'БӨЖ тесттер'

# Модель Тапсырмы
class TaskName(models.Model):
    topic = models.ForeignKey(TopicName, related_name="tasks", on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Номер тапсырмы")
    title = models.CharField("Название задания", max_length=255)
    description = models.TextField("Описание или инструкции", blank=True)
    image = models.ImageField("Рисунок (если есть)", upload_to='tasks/images/', blank=True, null=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"{self.number}-тапсырма: {self.title}"


class IWS(models.Model):
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'БӨЖ тақырыптары'
        verbose_name_plural = 'БӨЖ тақырыптары'


class ExamQuestion(models.Model):
    number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Емтихан сұрақтары'
        verbose_name_plural = 'Емтихан сұрақтары'