from django.db import models
import uuid
from apps.teachers.models import Teacher
from apps.subjects.models import Subject
from apps.classes.models import Class
from apps.students.models import Student
from apps.auth.models import User

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class FileUpload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    mime_type = models.CharField(max_length=100)
    minio_key = models.CharField(max_length=500, unique=True)
    file_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'file_uploads'

    def __str__(self):
        return f"{self.file_name} ({self.uploaded_by})"

class Assignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField(blank=True)
    due_date = models.DateTimeField()
    attachments = models.JSONField(default=list, blank=True)  # List of FileUpload IDs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'assignments'

    def __str__(self):
        return f"{self.title} - {self.class_assigned}"

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_files = models.JSONField(default=list, blank=True)  # List of FileUpload IDs
    submitted_at = models.DateTimeField(null=True, blank=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'assignment_submissions'
        unique_together = ['assignment', 'student']

    def __str__(self):
        return f"{self.student} - {self.assignment}"