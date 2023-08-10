from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Course(models.Model):
    '''модель курса'''
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='course/', verbose_name='картинка', **NULLABLE)


    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = "курсы"
        ordering = ('title',)


class Lesson(models.Model):
    '''модель урока'''
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='картинка', **NULLABLE)
    link_to_video = models.CharField(max_length=150, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', null=True)

    def __str__(self):
        return f'{self.title}, {self.course}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = "уроки"
        ordering = ('title',)


class Payments(models.Model):
    '''модель платежей'''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)

    payment_amount = models.PositiveIntegerField(default=0, verbose_name='сумма платежа')
    payment_way = models.CharField(max_length=50, verbose_name='способ оплаты')


    def __str__(self):
        return f'{self.owner}, {self.date}, {self.course if self.course else self.lesson}, {self.payment_amount}, {self.payment_way}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = "оплаты"
        ordering = ('owner',)