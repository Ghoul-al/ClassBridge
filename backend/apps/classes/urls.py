from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SectionViewSet, ArmViewSet, ClassViewSet

router = DefaultRouter()
router.register(r'sections', SectionViewSet)
router.register(r'arms', ArmViewSet)
router.register(r'classes', ClassViewSet)

urlpatterns = [
    path('', include(router.urls)),
]