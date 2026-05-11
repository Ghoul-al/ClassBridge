from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, QuestionViewSet, ChoiceViewSet, ExamAttemptViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'attempts', ExamAttemptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]