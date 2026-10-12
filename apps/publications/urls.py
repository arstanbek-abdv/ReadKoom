from rest_framework import routers
from django.urls import path, include
from apps.publications.views import UploadFile, PublicationDraft

publication_draft_router = routers.SimpleRouter()

publication_draft_router.register(r'drafts', 
    PublicationDraft,basename='publication-draft'
)

urlpatterns = [
    path('', include(publication_draft_router.urls)),
    path('drafts/<int:pk>/attachments/',
        UploadFile.as_view(),name='file-upload'
    ),
]
