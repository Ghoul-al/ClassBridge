from django.db import models
import uuid

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Subject(models.Model):
    STREAM_CHOICES = [
        ('science', 'Science'),
        ('commercial', 'Commercial'),
        ('arts', 'Arts'),
        ('general', 'General'),  # For primary/junior
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    stream = models.CharField(max_length=20, choices=STREAM_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'subjects'
        unique_together = ['school_id', 'code']

    def __str__(self):
        return f"{self.name} ({self.code})"