from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.publications.models import File

class UploadFileSerializer(ModelSerializer):
    
    class Meta:
        model = File
        fields = [
            'file_name',
            'file_key',
            'file_mime',
            'publication',
            'upload_status'
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'file_key',
            'file_mime',
            'upload_status'
            'created_at',
            'updated_at'
        ]
    