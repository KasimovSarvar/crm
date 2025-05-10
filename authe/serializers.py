from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',  'password' , 'full_name', 'fixed_salary' , 'phone_number' , 'status' , 'lead_number', 'login_time')

