from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.publications.models import Publication

class UploadFileSerializer(ModelSerializer):
    
    class Meta:
        model = Publication
        fields = [
            'title',
            'description',
            'file_name',
            'file_key',
            'user',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'file_key',
            'user',
            'created_at',
            'updated_at'
        ]