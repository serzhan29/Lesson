# Generated by Django 4.2.15 on 2024-09-24 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_answer_options_alter_studentsubmission_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answer_count',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество ответов'),
        ),
    ]
