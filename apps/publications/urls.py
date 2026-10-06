from django.urls import path 
from apps.publications.views import UploadFile

urlpatterns = [
    path('upload/',UploadFile.as_view()),
]