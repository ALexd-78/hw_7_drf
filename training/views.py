from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from training.models import Course, Lesson, Payments, Subscription
from training.paginators import TrainingPaginator
from training.permissions import IsOwnerOrStaff, IsOwner
from training.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer, \
    PaymentIntentCreateSerializer, PaymentIntentConfirmSerializer
from training.services import PaymentService


class CourseViewSet(viewsets.ModelViewSet):
    '''viewset for course'''
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]
    pagination_class = TrainingPaginator


class LessonCreateAPIView(generics.CreateAPIView):
    '''Lesson create endpoint'''
    serializer_class = LessonSerializer
    # permission_classes = [IsOwner]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # переопределение метода создания объекта класса только для авторизованного пользователя
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

class LessonListAPIView(generics.ListAPIView):
    '''Lesson list endpoint'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]
    pagination_class = TrainingPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    '''Lesson retrive endpoint'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    '''Lesson updaate endpoint'''
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    '''Lesson delete endpoint'''
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    '''Создание платежа'''
    serializer_class = PaymentsSerializer


class PaymentListAPIView(generics.ListAPIView):
    '''Payment list endpoint'''
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['date']


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    '''Просмотр одного платежа'''
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsOwnerOrStaff]

class SubscriptionCreateAPIView(generics.CreateAPIView):
    '''Subscription create endpoint'''
    serializer_class = SubscriptionSerializer


class SubscriptionListAPIView(generics.ListAPIView):
    '''Subscription list endpoint'''
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    '''Subscription retrive endpoint'''
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    '''Subscription delete endpoint'''
    queryset = Subscription.objects.all()


class PaymentIntentCreateView(generics.CreateAPIView):
    '''Создание платежного намерения'''
    serializer_class = PaymentIntentCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user = self.request.user
            try:
                payment_intent = PaymentService.create_payment_intent(course_id=course_id, user=user)
                payment = Payments.objects.filter(id_payment_intent=payment_intent['id']).first()
                payment_serializer = PaymentsSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PaymentIntentConfirmView(generics.CreateAPIView):
    '''Подтверждение платежа'''
    serializer_class = PaymentIntentConfirmSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_payment_intent = serializer.validated_data['id_payment_intent']
            payment_token = serializer.validated_data['payment_token']
            try:
                # создание метода платежа
                payment_method = PaymentService.create_payment_method(payment_token)
                # привязка метода платежа к платежному намерению
                PaymentService.connect_payment_intent_and_method(payment_method_id=payment_method["id"],
                                                                 id_payment_intent=id_payment_intent)
                # подтверждение платежа
                PaymentService.confirm_payment_intent(id_payment_intent)
                payment = Payments.objects.filter(id_payment_intent=id_payment_intent).first()
                # изменение статуса платежа на "Оплачено"
                payment.change_is_paid()
                payment_serializer = PaymentsSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
