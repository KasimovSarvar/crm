from django.db.transaction import rollback
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from authe.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'role', 'fixed_salary', 'phone_number', 'status', 'lead_number', 'login_time')