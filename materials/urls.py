from django.urls import path

from materials.apps import MaterialsConfig
from rest_framework.routers import SimpleRouter

from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonUpdateAPIView, \
    LessonDeleteAPIView, LessonRetrieveAPIView

router = SimpleRouter()
router.register(r'course', CourseViewSet, basename='courses')

app_name = MaterialsConfig.name
urlpatterns = [
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
               ] + router.urls
