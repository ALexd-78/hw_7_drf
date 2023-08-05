from rest_framework import serializers

from training.models import Course, Lesson
from users.models import User


class CourseSerializer(serializers.ModelSerializer):
    '''сериализатор курса'''
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    '''сериализатор курса'''
    class Meta:
        model = Lesson
        fields = '__all__'