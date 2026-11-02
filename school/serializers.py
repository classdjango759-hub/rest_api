from rest_framework import serializers
from school.models import School

# Serializer
# ModelSerializer
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = "__all__"

    def validate_name(self, value:str):
        if not value.isalpha():
            raise serializers.ValidationError("Only alphabet is allowed")
        return value
    
    def validate_established_since(self, value):
        year_str = str(value)
        if len(year_str) != 4:
            raise serializers.ValidationError("Only four characters allowed")
        return value


class UpdateSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['avg_student_per_year', 'is_accredited']


class EstablishedSinceSerializer(serializers.Serializer):
    established_year = serializers.IntegerField()

    def validate_established_year(self, value):
        year_str = str(value)
        if len(year_str) != 4:
            raise serializers.ValidationError("Year must be exactly 4 characters")
        return value
