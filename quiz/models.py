import uuid
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=500)

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    CORRECT_OPTIONS = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    correct_option = models.CharField(
        max_length=1,
        choices=CORRECT_OPTIONS
    )

    def __str__(self):
        return self.question_text


class QuizAttempt(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)

    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()

    passed = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score}/{self.total_questions}"


class Certificate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    score = models.PositiveIntegerField()

    certificate_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.certificate_id}"
