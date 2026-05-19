from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers 

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
    
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate_password(self,value):
        validate_password(value,self.instance)
        return value 
    
    def create(self,validated_data):
        password = validated_data.pop('password') # we pop out the password 
        user = User(**validated_data) # we instantiate the user with the remaining fields 
        user.set_password(password) # we turn the raw password into hash and save it to user object along with other fields 
        user.save() # we write the object to DB 
        return user 
        