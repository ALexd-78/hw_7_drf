from rest_framework import serializers

from training.serializers import PaymentsSerializer
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    '''сериализатор пользователя'''

    '''поле вывода всех платежей пользователя'''
    payments = PaymentsSerializer(many=True, source='payments_set', default=0, read_only=True)

    class Meta:
        model = User
        fields = '__all__'