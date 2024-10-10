from django.urls import path

from .views import hello, translate_text

urlpatterns = [
    path('translate/', translate_text, name='translate_text'),
    path('hello/', hello, name='hello'),
]
