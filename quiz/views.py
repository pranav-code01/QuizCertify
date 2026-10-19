
import io
import qrcode

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

from .models import Question, Certificate, QuizAttempt


def quiz_home(request):
    questions = Question.objects.all()

    return render(request, 'quiz/quiz_home.html', {
        'questions': questions
    })


# Admin Dashboard
@user_passes_test(lambda user: user.is_staff)
def dashboard(request):
    total_attempts = QuizAttempt.objects.count()

    passed_count = QuizAttempt.objects.filter(
        passed=True
    ).count()

    failed_count = QuizAttempt.objects.filter(
        passed=False
    ).count()

    total_certificates = Certificate.objects.count()

    recent_attempts = QuizAttempt.objects.order_by(
        '-attempted_at'
    )[:20]

    context = {
        'total_attempts': total_attempts,
        'passed_count': passed_count,
        'failed_count': failed_count,
        'total_certificates': total_certificates,
        'recent_attempts': recent_attempts,
    }

    return render(
        request,
        'quiz/dashboard.html',
        context
    )


def generate_certificate_pdf(certificate, request):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setTitle("Python Quiz Certificate")
    pdf.setStrokeColorRGB(0.1, 0.4, 0.7)
    pdf.setLineWidth(3)
    pdf.rect(25, 25, 545, 790)

    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawCentredString(
        297, 740, "CERTIFICATE OF ACHIEVEMENT"
    )

    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(
        297, 690, "This certificate is presented to"
    )

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawCentredString(
        297, 645, certificate.name
    )

    pdf.setFont("Helvetica", 13)
    pdf.drawCentredString(
        297, 600,
        "For successfully completing the Python Quiz"
    )

    pdf.drawCentredString(
        297, 570,
        f"Score: {certificate.score}/10"
    )

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        40, 70,
        f"Certificate ID: {certificate.certificate_id}"
    )

    verify_url = request.build_absolute_uri(
        reverse(
            'verify_certificate',
            args=[certificate.certificate_id]
        )
    )

    qr_image = qrcode.make(verify_url)
    qr_buffer = io.BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    pdf.drawImage(
        ImageReader(qr_buffer),
        455, 80,
        width=85,
        height=85
    )

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="certificate_'
        f'{certificate.certificate_id}.pdf"'
    )

    return response


@require_POST
def submit_quiz(request):
    questions = Question.objects.all()

    name = request.POST.get('name', '').strip()
    mobile = request.POST.get('mobile', '').strip()
    email = request.POST.get('email', '').strip()

    if not name or not mobile or not email:
        return render(request, 'quiz/quiz_home.html', {
            'questions': questions,
            'error': 'Please fill in all student details.'
        })

    if not mobile.isdigit() or len(mobile) != 10:
        return render(request, 'quiz/quiz_home.html', {
            'questions': questions,
            'error': 'Please enter a valid 10-digit mobile number.'
        })

    total = questions.count()

    if total == 0:
        return render(request, 'quiz/quiz_home.html', {
            'questions': questions,
            'error': 'No questions are available.'
        })

    score = 0

    for question in questions:
        answer = request.POST.get(
            f'question_{question.id}', ''
        )

        if answer not in ['A', 'B', 'C', 'D']:
            return render(request, 'quiz/quiz_home.html', {
                'questions': questions,
                'error': (
                    'Please answer all questions before submitting.'
                )
            })

        if answer == question.correct_option:
            score += 1

    passed = score >= 7
    certificate = None
    email_sent = False
    email_error = False

    # Save every attempt, whether pass or fail.
    attempt = QuizAttempt.objects.create(
        name=name,
        email=email,
        mobile=mobile,
        score=score,
        total_questions=total,
        passed=passed,
        email_sent=False,
    )

    if passed:
        certificate = Certificate.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            score=score
        )

        try:
            pdf_response = generate_certificate_pdf(
                certificate, request
            )

            email_message = EmailMessage(
                subject="Your Python Quiz Certificate",
                body=(
                    f"Hello {name},\n\n"
                    "Congratulations! You have passed "
                    "the Python Quiz.\n"
                    f"Your score is {score}/{total}.\n"
                    "Your certificate PDF is attached "
                    "to this email.\n\n"
                    "Thank you!"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )

            email_message.attach(
                f"certificate_{certificate.certificate_id}.pdf",
                pdf_response.content,
                "application/pdf",
            )

            email_message.send(fail_silently=True)
            email_sent = True

            attempt.email_sent = True
            attempt.save(update_fields=['email_sent'])

        except Exception as error:
            print("Certificate email error:", error)
            email_error = True

    return render(request, 'quiz/result.html', {
        'name': name,
        'score': score,
        'total': total,
        'passed': passed,
        'certificate': certificate,
        'email_sent': email_sent,
        'email_error': email_error,
    })


def download_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(
            certificate_id=certificate_id
        )
    except Certificate.DoesNotExist:
        return HttpResponse(
            "Certificate not found.",
            status=404
        )

    return generate_certificate_pdf(certificate, request)


def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(
            certificate_id=certificate_id
        )
    except Certificate.DoesNotExist:
        return HttpResponse(
            "Invalid certificate.",
            status=404
        )

    return render(request, 'quiz/verify_certificate.html', {
        'certificate': certificate
    })