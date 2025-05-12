from rest_framework import serializers
from .models import Lead, Student
from authe.models import User 

class LeadSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lead
        fields = ['id', 'admin', 'first_name', 'last_name', 'phone_number', 'status', 'type', 'is_checked', 'is_signing_at']
        read_only_fields = ['admin']


class StudentSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Student
        fields = ['id', 'admin', 'first_name', 'last_name', 'phone_number', 'passport_series', 'education_type', 'faculty', 'study_format']
        read_only_fields = ['admin']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
