from django.urls import path

from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, SubscriptionListAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionDeleteAPIView

app_name = TrainingConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),

    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscription/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription_retrieve'),
    path('subscription/delete/<int:pk>/', SubscriptionDeleteAPIView.as_view(), name='subscription_delete')

] + router.urls