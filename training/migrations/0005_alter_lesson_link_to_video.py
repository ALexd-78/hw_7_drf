# Generated by Django 4.2.4 on 2023-08-18 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0004_alter_course_options_alter_lesson_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='link_to_video',
            field=models.URLField(blank=True, max_length=150, null=True, verbose_name='ссылка на видео'),
        ),
    ]