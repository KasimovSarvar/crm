from .models import Lead,Student
from rest_framework.serializers import ModelSerializer


class LeadSerializer(ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'







