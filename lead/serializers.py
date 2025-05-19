from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Outcome, CategoryOutlay, Payment, Student, SeasonFacultyLimit, Season, Faculty, University, State, \
    Comment, Lead

class OutcomeSerializer(ModelSerializer):
    class Meta:
        model = Outcome
        fields = ('id', 'accountant', 'category', 'description', 'amount', 'type')

class CategoryOutlaySerializer(ModelSerializer):
    class Meta:
        model = CategoryOutlay
        fields = ('id', 'name', 'limit')

class PaymentCreateSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'student', 'type', 'uploader_amount', 'amount', 'check_file', 'comment')

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        read_only_fields = ['check_uploader', 'confirmatory']
        fields = ('id', 'student', 'check_uploader', 'confirmatory', 'type', 'uploader_amount', 'amount', 'check_file', 'is_payed', 'comment')

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'admin', 'state', 'university', 'season', 'education_type', 'faculty', 'study_format', 'first_name', 'last_name', 'phone_number', 'passport_series')

        read_only_fields = ['created_by', 'id', 'admin']

class SeasonFacultyLimitSerializer(ModelSerializer):
    class Meta:
        model = SeasonFacultyLimit
        fields = ('id', 'season', 'faculty', 'grant', 'contract', 'evening', 'extramural')

class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'state', 'university', 'name', 'start_date', 'end_date', 'closed')

class FacultySerializer(ModelSerializer):
    class Meta:
        model = Faculty
        fields = ('id', 'name', 'university', 'education_type', 'grant', 'contract', 'evening', 'extramural')

class UniversitySerializer(ModelSerializer):
    class Meta:
        model = University
        fields = ('id', 'state', 'name')

class StateSerializer(ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'admin','lead', 'comment', 'lead_status')

class LeadSerializer(ModelSerializer):
    is_checked = serializers.BooleanField(default=False)
    class Meta:
        model = Lead
        fields = ('id', 'admin', 'first_name', 'last_name', 'passport_series', 'phone_number', 'status', 'type', 'is_checked', 'is_signing_at')
        read_only_fields = ['id', 'admin']