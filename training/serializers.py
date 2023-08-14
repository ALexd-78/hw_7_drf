from rest_framework import serializers

from training.models import Course, Lesson, Payments
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    '''сериализатор урока'''
    class Meta:
        model = Lesson
        fields = '__all__'


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


