from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.models import User
from apps.publications.serializers import UploadFileSerializer
from apps.publications.models import Publication

from services.storage import generate_file_key, upload_url

class UploadFile(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UploadFileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        file_key = generate_file_key(request.user)
        upload_link = upload_url(file_key)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user = request.user,
            file_key = file_key
        )
        return Response(
            {
                'upload_url': upload_link
            },
            status = status.HTTP_201_CREATED
        )