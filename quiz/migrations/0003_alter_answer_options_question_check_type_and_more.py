# Generated by Django 4.2.15 on 2024-09-21 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0002_alter_answer_options_answer_filled_cells_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Жауап', 'verbose_name_plural': 'Жауаптар'},
        ),
        migrations.AddField(
            model_name='question',
            name='check_type',
            field=models.CharField(choices=[('auto', 'Автоматическая проверка'), ('manual', 'Ручная проверка')], default='auto', max_length=50, verbose_name='Тип проверки'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='filled_cells',
            field=models.JSONField(blank=True, null=True, verbose_name='Толтырылған ұяшықтар'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='Дұрыс жауап'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='reordered_items',
            field=models.JSONField(blank=True, null=True, verbose_name='Қайта реттелген элементтер'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Жауап'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('text', 'Текстовое поле'), ('table', 'Таблица'), ('reorder', 'Перестановка')], max_length=50, verbose_name='Сұрақ түрі'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=500, verbose_name='Сұрақ'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='allow_multiple_answers',
            field=models.BooleanField(default=False, verbose_name='Бірнеше жауап беруге рұқсат етіңіз'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Тест атауы'),
        ),
        migrations.AlterField(
            model_name='userquizresult',
            name='score',
            field=models.FloatField(blank=True, null=True, verbose_name='Баллы'),
        ),
        migrations.CreateModel(
            name='UserQuizAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(blank=True, null=True, verbose_name='Ответ студента')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('is_correct', models.BooleanField(blank=True, null=True, verbose_name='Ответ верный')),
                ('checked_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата проверки')),
                ('checked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checked_answers', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='quiz.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ответ студента',
                'verbose_name_plural': 'Ответы студентов',
            },
        ),
    ]
