from django.db import models
import uuid
from apps.auth.models import User
from apps.classes.models import Class

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    admission_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'students'
        unique_together = ['school_id', 'admission_number']

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.admission_number})"