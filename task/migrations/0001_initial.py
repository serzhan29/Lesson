# Generated by Django 4.2.15 on 2024-09-24 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Тапсырма атауы: ')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Сипаттама')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Құрылған күні')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пайдаланушы жасаған')),
            ],
            options={
                'verbose_name': 'Тапсырма ',
                'verbose_name_plural': 'Тапсырмалар',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='Сұрақ мәтіні')),
                ('question_type', models.CharField(choices=[('text', 'Текстовое поле'), ('choice', 'Один выбор'), ('multichoice', 'Множественный выбор')], max_length=20, verbose_name='Сұрақ түрі')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='task.assignment', verbose_name='Тапсырма')),
            ],
            options={
                'verbose_name': 'Сұрақ ',
                'verbose_name_plural': 'Сұрақтар ',
            },
        ),
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='task.assignment', verbose_name='Задание')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Студент')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
                'unique_together': {('student', 'assignment')},
            },
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Жауап')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task.question', verbose_name='Сұрақ')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='task.studentsubmission', verbose_name='Студенттің жауабы')),
            ],
            options={
                'verbose_name': 'Студенттердің жауабы',
                'verbose_name_plural': 'Студенттердің жауаптары',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField(verbose_name='Жауап')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='task.question', verbose_name='Сұрақ')),
            ],
            options={
                'verbose_name': 'Жауаб',
                'verbose_name_plural': 'Жауаптар',
            },
        ),
    ]
