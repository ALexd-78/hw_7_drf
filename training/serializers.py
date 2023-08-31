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
    '''Сериализатор представление модели Подписка'''

    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentIntentCreateSerializer(serializers.Serializer):
    '''Сериализатор для создания намерения платежа'''
    course_id = serializers.IntegerField()

    @staticmethod
    def validate_course_id(value):
        '''Проверяет, существует ли курс с таким ID'''
        course = Course.objects.filter(id=value)
        if not course:
            raise serializers.ValidationError(f'Курса {value} не существует')
        return value


class PaymentMethodCreateSerializer(serializers.Serializer):
    '''Сериализатор для создания метода платежа'''
    payment_token = serializers.CharField(max_length=300)


class PaymentIntentConfirmSerializer(serializers.Serializer):
    '''Сериализатор для подтверждения платежа'''
    id_payment_intent = serializers.CharField(max_length=300)
    payment_token = serializers.CharField(max_length=300)

    @staticmethod
    def validate_id_payment_intent(value):
        '''Проверяет, существует ли курс с таким ID'''
        payment = Payments.objects.filter(id_payment_intent=value).first()
        if payment.is_paid:
            raise serializers.ValidationError(f'Платеж с ID={value} уже подтвержден')
        if not payment:
            raise serializers.ValidationError(f'Созданного платежа с ID={value} не существует')
        return value