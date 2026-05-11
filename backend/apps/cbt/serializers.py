from rest_framework import serializers
from .models import Exam, Question, Choice, ExamAttempt, StudentAnswer

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'order']
        read_only_fields = ['id']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'marks', 'order', 'choices']
        read_only_fields = ['id']

class ExamSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_assigned.name', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name', 'class_assigned', 'class_name', 'title', 'description', 'duration', 'total_marks', 'randomize_questions', 'is_active', 'question_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_question_count(self, obj):
        return obj.questions.count()

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class ExamAttemptSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    time_elapsed = serializers.SerializerMethodField()

    class Meta:
        model = ExamAttempt
        fields = ['id', 'exam', 'exam_title', 'student', 'student_name', 'started_at', 'submitted_at', 'score', 'status', 'time_remaining', 'time_elapsed']
        read_only_fields = ['id', 'started_at', 'score']

    def get_time_elapsed(self, obj):
        from django.utils import timezone
        if obj.submitted_at:
            return int((obj.submitted_at - obj.started_at).total_seconds())
        return int((timezone.now() - obj.started_at).total_seconds())

class StudentAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    selected_choice_text = serializers.CharField(source='selected_choice.choice_text', read_only=True)

    class Meta:
        model = StudentAnswer
        fields = ['id', 'question', 'question_text', 'selected_choice', 'selected_choice_text', 'answer_text', 'is_correct', 'marks_obtained', 'answered_at']
        read_only_fields = ['id', 'is_correct', 'marks_obtained', 'answered_at']

class ExamDetailSerializer(ExamSerializer):
    """Serializer for exam details including questions"""
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(ExamSerializer.Meta):
        fields = ExamSerializer.Meta.fields + ['questions']

class ExamAttemptDetailSerializer(ExamAttemptSerializer):
    """Serializer for attempt details including answers"""
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta(ExamAttemptSerializer.Meta):
        fields = ExamAttemptSerializer.Meta.fields + ['answers']