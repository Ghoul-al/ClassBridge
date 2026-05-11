from django.db import models
import uuid
from apps.auth.models import User
from apps.classes.models import Class
from apps.subjects.models import Subject

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.CharField(max_length=100, blank=True)
    employment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.department})"

class TeacherSubject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)  # Optional specific class
    assigned_date = models.DateField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'teacher_subjects'
        unique_together = ['teacher', 'subject', 'class_assigned']

    def __str__(self):
        class_info = f" - {self.class_assigned}" if self.class_assigned else ""
        return f"{self.teacher} - {self.subject}{class_info}"

class TeacherClass(models.Model):
    ROLE_CHOICES = [
        ('class_teacher', 'Class Teacher'),
        ('subject_teacher', 'Subject Teacher'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='class_assignments')
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='subject_teacher')
    assigned_date = models.DateField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'teacher_classes'
        unique_together = ['teacher', 'class_assigned']

    def __str__(self):
        return f"{self.teacher} - {self.class_assigned} ({self.role})"