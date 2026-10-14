from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.publications.serializers import UploadFileSerializer, PublicationSerializer
from apps.publications.models import Publication
from apps.publications.exceptions import FileAlreadyExists
from services.storage import generate_file_key, upload_url

class PublicationDraft(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PublicationSerializer
    queryset = Publication.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        publication = get_object_or_404(self.queryset, 
            pk=pk, author=request.user
        )
        publication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        publication = get_object_or_404(self.queryset, 
            pk=pk, author=request.user
        )
        serializer = self.get_serializer(publication, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        publication = get_object_or_404(self.queryset, 
            pk=pk, author=request.user
        )
        serializer = self.get_serializer(publication, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadFile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer

    def create(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        publication = get_object_or_404(Publication, 
            pk=pk, author=request.user
        )
        serializer = self.get_serializer(data=request.data)
        file_key = generate_file_key(request.user)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(file_key = file_key, publication=publication)
            mime_type = serializer.validated_data['mime_type']
            upload_link = upload_url(file_key=file_key, mime_type=mime_type)
        except IntegrityError:
            raise FileAlreadyExists()
        return Response(
            {'file':serializer.data, 'upload_url': upload_link},
            status = status.HTTP_201_CREATED
        )
    