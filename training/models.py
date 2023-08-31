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
    link_to_video = models.URLField(max_length=150, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', null=True)

    def __str__(self):
        return f'{self.title}, {self.course}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = "уроки"
        ordering = ('title',)


class Payments(models.Model):
    '''модель платежей'''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE)

    payment_amount = models.PositiveIntegerField(default=0, verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=50, verbose_name='способ оплаты') # наличные или перевод на счет.

    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    id_intent = models.CharField(max_length=300, verbose_name='id_намерение платежа', **NULLABLE)
    id_method = models.CharField(max_length=300, verbose_name='id_метод платежа', **NULLABLE)
    status = models.CharField(max_length=50, verbose_name='статус платежа', **NULLABLE)


    def __str__(self):
        return f'{self.owner}, {self.date}, {self.course if self.course else self.lesson}, {self.payment_amount}, {self.payment_way}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = "оплаты"
        ordering = ('owner',)


class Subscription(models.Model):
    """
        модель подписки на курс
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    is_active = models.BooleanField(default=False, verbose_name='статус подписки')
    version = models.CharField(max_length=100, default=1, verbose_name='версия подписки')

    def __str__(self):
        return f'Подписка на курс {self.course} ({self.owner})'

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курсы'
        ordering = ('owner', 'course',)

    def delete(self, **kwargs):
        """Отключение подписки"""
        self.is_active = False
        self.save()

    def update_version(self, version):
        self.version = version
        self.save()

    def activate(self):
        self.is_active = True
        self.save()