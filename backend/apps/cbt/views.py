from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Exam, Question, Choice, ExamAttempt, StudentAnswer
from .serializers import (
    ExamSerializer, ExamDetailSerializer,
    QuestionSerializer, ChoiceSerializer,
    ExamAttemptSerializer, ExamAttemptDetailSerializer,
    StudentAnswerSerializer
)

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(school_id=self.request.school_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamDetailSerializer
        return ExamSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(exam__school_id=self.request.school_id)
        return queryset

class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(question__exam__school_id=self.request.school_id)
        return queryset

class ExamAttemptViewSet(viewsets.ModelViewSet):
    queryset = ExamAttempt.objects.all()
    serializer_class = ExamAttemptSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self.request, 'school_id') and self.request.school_id:
            return queryset.filter(exam__school_id=self.request.school_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExamAttemptDetailSerializer
        return ExamAttemptSerializer

    @action(detail=False, methods=['post'])
    def start_exam(self, request):
        """Start an exam attempt for a student"""
        exam_id = request.data.get('exam_id')
        if not exam_id:
            return Response({'error': 'exam_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            exam = Exam.objects.get(id=exam_id, school_id=request.school_id)
        except Exam.DoesNotExist:
            return Response({'error': 'Exam not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if student already has an attempt
        attempt, created = ExamAttempt.objects.get_or_create(
            exam=exam,
            student=request.user.student_profile,
            defaults={'time_remaining': exam.duration * 60}  # Convert to seconds
        )

        if not created and attempt.status != 'in_progress':
            return Response({'error': 'Exam already completed'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(attempt)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        """Submit or update an answer for a question"""
        attempt = self.get_object()
        question_id = request.data.get('question_id')
        choice_id = request.data.get('choice_id')

        if not question_id:
            return Response({'error': 'question_id required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Question.objects.get(id=question_id, exam=attempt.exam)
        except Question.DoesNotExist:
            return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

        choice = None
        if choice_id:
            try:
                choice = Choice.objects.get(id=choice_id, question=question)
            except Choice.DoesNotExist:
                return Response({'error': 'Choice not found'}, status=status.HTTP_404_NOT_FOUND)

        answer, created = StudentAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={'selected_choice': choice}
        )

        serializer = StudentAnswerSerializer(answer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def submit_exam(self, request, pk=None):
        """Submit the entire exam"""
        attempt = self.get_object()
        if attempt.status != 'in_progress':
            return Response({'error': 'Exam already submitted'}, status=status.HTTP_400_BAD_REQUEST)

        attempt.submitted_at = timezone.now()
        attempt.status = 'completed'
        attempt.calculate_score()
        attempt.save()

        serializer = self.get_serializer(attempt)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_questions(self, request, pk=None):
        """Get randomized questions for the student"""
        attempt = self.get_object()
        questions = attempt.exam.get_randomized_questions(attempt.student)

        data = []
        for question in questions:
            choices = question.get_randomized_choices(attempt.student)
            question_data = QuestionSerializer(question).data
            question_data['choices'] = ChoiceSerializer(choices, many=True).data
            data.append(question_data)

        return Response(data)