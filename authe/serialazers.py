from rest_framework.serializers import ModelSerializer
from .models import User

from lead.models import Lead,Student


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password","full_name","role","fixed_salary","phone_number","status","lead_number")


