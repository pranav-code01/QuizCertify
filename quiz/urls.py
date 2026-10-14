
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),

    path('submit/', views.submit_quiz, name='submit_quiz'),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'certificate/<uuid:certificate_id>/',
        views.download_certificate,
        name='download_certificate'
    ),

    path(
        'verify/<uuid:certificate_id>/',
        views.verify_certificate,
        name='verify_certificate'
    ),
]