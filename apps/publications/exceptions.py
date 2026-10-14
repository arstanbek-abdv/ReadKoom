from rest_framework.exceptions import APIException

class FileAlreadyExists(APIException):
    status_code = 409
    default_detail = 'Publication already has a file'
    default_code = 'file_already_exists'