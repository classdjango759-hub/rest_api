from rest_framework import serializers
from django.contrib.auth.models import User

# Serializer
# ModelSerializer

class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    # Validation
    # def validate_FIELDNAME(self, value):
    def validate_username(self, value):
        if  "!" in value:
            raise serializers.ValidationError("Username should not contain '!'")
        return value

class UserModelSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
    
    def validate(self, attrs):
        data = super().validate(attrs)
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class ChangeUserFullName(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()


"""
RESPONSE BODY
{
 "username": "codezero",
 "email": "codezero@email.com",
 "first_name": "Code",
 "last_name": "Zero"
}

ENDPOINT:
    /api/user
"""


"""
    Model: Student
    Fields:
        - name: CharField
        - age: IntegerField
        - email: EmailField
        - department: CharField
        - enrollment_date: DateField

    Endpoints
    api/students/ [GET, POST]
    api/students/<int:id>/ [GET, PUT, DELETE]

    
"""