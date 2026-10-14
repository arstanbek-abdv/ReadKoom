from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.publications.models import File, Publication
from config.settings import ALLOWED_MIME_TYPE
import mimetypes

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

    def validate(self, attrs):
        mime_type, _ = mimetypes.guess_file_type(attrs['file_name']) # retrieving file type from file_name
        if mime_type not in ALLOWED_MIME_TYPE: # checking if it's allowed type 
            raise serializers.ValidationError(
                {'file_name':'Unsupported file type!'}
            )
        attrs['mime_type'] = mime_type # modifies dict in memory
        return attrs # passes back to validated_data 
    
    class Meta:
        model = File
        fields = [
            'file_name',
            'file_key',
            'publication',
            'mime_type',
            'file_size',
            'upload_status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'file_key',
            'publication',
            'mime_type',
            'upload_status',
            'created_at',
            'updated_at'
        ]

    

    