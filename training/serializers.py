from rest_framework import serializers

from training.models import Course


class CourseSerializer(serializers.ModelSerializer):
    '''сериализатор курса'''
    class Meta:
        model = Course
        fields = '__all__'