from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, ParentStudentViewSet

router = DefaultRouter()
router.register(r'parents', ParentViewSet)
router.register(r'parent-students', ParentStudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]