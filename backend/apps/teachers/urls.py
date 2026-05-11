from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, TeacherSubjectViewSet, TeacherClassViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'teacher-subjects', TeacherSubjectViewSet)
router.register(r'teacher-classes', TeacherClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]