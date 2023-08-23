from rest_framework import serializers

from training.models import Course, Lesson, Payments, Subscription
from training.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    '''сериализатор урока'''
    class Meta:
        model = Lesson
        fields = '__all__'
        validators =[
            LinkValidator(field='link_to_video'),
        ]


class CourseSerializer(serializers.ModelSerializer):
    '''сериализатор курса'''

    '''поле вывода всех уроков в курсе'''
    lessons = LessonSerializer(many=True, source='lesson_set', read_only=True)

    '''поле для вывода количества уроков в курсе'''
    lesson_count = serializers.IntegerField(source='lesson_set.count', default=0, read_only=True)
    class Meta:
        model = Course
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    '''сериализатор оплаты'''

    class Meta:
        model = Payments
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Сериализатор представление модели Подписка
    """

    class Meta:
        model = Subscription
        fields = '__all__'