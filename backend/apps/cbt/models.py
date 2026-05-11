from django.db import models
import uuid
from apps.teachers.models import Teacher
from apps.subjects.models import Subject
from apps.classes.models import Class
from apps.students.models import Student
from apps.auth.models import User
import random

class SchoolScopedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school_id = models.UUIDField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    total_marks = models.PositiveIntegerField()
    randomize_questions = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'exams'
        indexes = [
            models.Index(fields=['school_id']),
            models.Index(fields=['class_assigned']),
        ]

    def __str__(self):
        return f"{self.title} - {self.class_assigned}"

    def get_randomized_questions(self, student):
        """Get randomized questions for a student"""
        questions = list(self.questions.all())
        if self.randomize_questions:
            random.seed(str(student.id) + str(self.id))  # Consistent randomization per student
            random.shuffle(questions)
        return questions

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'questions'
        ordering = ['order']
        indexes = [
            models.Index(fields=['exam']),
        ]

    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

    def get_randomized_choices(self, student):
        """Get randomized choices for a student"""
        choices = list(self.choices.all())
        random.seed(str(student.id) + str(self.exam.id) + str(self.id))
        random.shuffle(choices)
        return choices

class Choice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'choices'
        ordering = ['order']

    def __str__(self):
        return f"Choice {self.order}: {self.choice_text[:30]}..."

class ExamAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('timed_out', 'Timed Out'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    time_remaining = models.PositiveIntegerField(null=True, blank=True)  # seconds

    objects = SchoolScopedManager()

    class Meta:
        db_table = 'exam_attempts'
        unique_together = ['exam', 'student']
        indexes = [
            models.Index(fields=['exam']),
            models.Index(fields=['student']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.student} - {self.exam} ({self.status})"

    def calculate_score(self):
        """Calculate and return the total score"""
        total_score = 0
        for answer in self.answers.all():
            if answer.is_correct:
                total_score += answer.question.marks
        self.score = total_score
        self.save()
        return total_score

class StudentAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    answer_text = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.PositiveIntegerField(default=0)
    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_answers'
        unique_together = ['attempt', 'question']
        indexes = [
            models.Index(fields=['attempt']),
            models.Index(fields=['question']),
        ]

    def __str__(self):
        return f"{self.attempt.student} - {self.question} - {'Correct' if self.is_correct else 'Incorrect'}"

    def save(self, *args, **kwargs):
        # Auto-determine if correct
        if self.selected_choice and self.selected_choice.is_correct:
            self.is_correct = True
            self.marks_obtained = self.question.marks
        else:
            self.is_correct = False
            self.marks_obtained = 0
        super().save(*args, **kwargs)