from django.db import models
import uuid

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        # This will be overridden in views to filter by request.school_id
        return super().get_queryset()

class Section(models.Model):
    SECTION_CHOICES = [
        ('PRIMARY', 'Primary'),
        ('JUNIOR_SECONDARY', 'Junior Secondary'),
        ('SENIOR_SECONDARY', 'Senior Secondary'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    name = models.CharField(max_length=20, choices=SECTION_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'sections'
        unique_together = ['school_id', 'name']

    def __str__(self):
        return self.name

class Arm(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'arms'
        unique_together = ['school_id', 'name']

    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    name = models.CharField(max_length=50)
    level = models.IntegerField()  # 1-6 for primary, 1-3 for secondary
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    arm = models.ForeignKey(Arm, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'classes'
        unique_together = ['school_id', 'name']

    def __str__(self):
        arm_name = f" {self.arm.name}" if self.arm else ""
        return f"{self.section.name} {self.level}{arm_name}"