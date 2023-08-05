from training.apps import TrainingConfig
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet

app_name = TrainingConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [

] + router.urls