from django.db import models

NULLABLE = {'blank': True, 'null': True}

class Course(models.Model):
    '''модель курса'''
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='картинка', **NULLABLE)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    '''модель урока'''
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='image/', verbose_name='картинка', **NULLABLE)
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', null=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = "уроки"

