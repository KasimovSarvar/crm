from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Outcome

class OutcomeSerializer(ModelSerializer):
    class Meta:
        model = Outcome
        fields = ('accountant', 'category', 'description', 'amount', 'type')