from django.contrib import admin
from .models import Question, Certificate, QuizAttempt


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'question_text',
        'correct_option',
    )
    search_fields = ('question_text',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'mobile',
        'score',
        'certificate_id',
        'issued_at',
    )
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('issued_at',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'mobile',
        'score',
        'total_questions',
        'passed',
        'email_sent',
        'attempted_at',
    )
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('passed', 'email_sent', 'attempted_at')
    ordering = ('-attempted_at',)
    readonly_fields = (
        'name',
        'email',
        'mobile',
        'score',
        'total_questions',
        'passed',
        'email_sent',
        'attempted_at',
    )

