# Generated by Django 4.2.4 on 2023-08-10 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0003_alter_course_preview_alter_lesson_preview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ('title',), 'verbose_name': 'курс', 'verbose_name_plural': 'курсы'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('title',), 'verbose_name': 'урок', 'verbose_name_plural': 'уроки'},
        ),
        migrations.AlterModelOptions(
            name='payments',
            options={'ordering': ('owner',), 'verbose_name': 'оплата', 'verbose_name_plural': 'оплаты'},
        ),
        migrations.RemoveField(
            model_name='payments',
            name='user',
        ),
        migrations.AddField(
            model_name='payments',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]