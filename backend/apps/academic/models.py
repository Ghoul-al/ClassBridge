from django.db import models
import uuid

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class AcademicSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    name = models.CharField(max_length=20, help_text="e.g., 2025/2026")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'academic_sessions'
        unique_together = ['school_id', 'name']

    def __str__(self):
        return self.name

class Term(models.Model):
    TERM_CHOICES = [
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, choices=TERM_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'terms'
        unique_together = ['session', 'name']

    def __str__(self):
        return f"{self.session.name} - {self.name}"