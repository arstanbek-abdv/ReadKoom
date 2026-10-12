from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.publications.models import File, Publication

class PublicationSerializer(ModelSerializer):
    
    class Meta:
        model = Publication
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at'
        ]


class UploadFileSerializer(ModelSerializer):
    
    class Meta:
        model = File
        fields = [
            'file_name',
            'file_key',
            'mime_type',
            'file_size',
            'upload_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'file_key',
            'mime_type',
            'upload_status'
            'created_at',
            'updated_at'
        ]