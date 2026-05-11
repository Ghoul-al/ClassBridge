from rest_framework import serializers
from django.utils import timezone
from .models import Assignment, AssignmentSubmission, FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file_name', 'file_size', 'mime_type', 'file_url', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

class AssignmentSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.user.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_name = serializers.CharField(source='class_assigned.name', read_only=True)
    attachments_details = FileUploadSerializer(source='attachments', many=True, read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'teacher', 'teacher_name', 'subject', 'subject_name', 'class_assigned', 'class_name', 'title', 'instructions', 'due_date', 'attachments', 'attachments_details', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['school_id'] = self.context['request'].school_id
        return super().create(validated_data)

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    submitted_files_details = FileUploadSerializer(source='submitted_files', many=True, read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'assignment_title', 'student', 'student_name', 'submitted_files', 'submitted_files_details', 'submitted_at', 'grade', 'feedback', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set submitted_at when status changes to submitted
        if validated_data.get('status') == 'submitted' and not validated_data.get('submitted_at'):
            validated_data['submitted_at'] = timezone.now()
        return super().create(validated_data)