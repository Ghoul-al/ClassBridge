from django.db import models
import uuid
from apps.auth.models import User
from apps.students.models import Student

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Parent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='guardian')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'parents'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.relationship})"

class ParentStudent(models.Model):
    RELATIONSHIP_CHOICES = [
        ('primary', 'Primary Guardian'),
        ('secondary', 'Secondary Guardian'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='student_relationships')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent_relationships')
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, default='primary')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'parent_students'
        unique_together = ['parent', 'student']

    def __str__(self):
        return f"{self.parent} - {self.student} ({self.relationship})"