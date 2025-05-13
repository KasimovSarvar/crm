from django.contrib import admin
from .models import (
    Lead, Comment, Season, State, Student, University,
    Faculty, SeasonFacultyLimit, Outcome, Payment, CategoryOutlay
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'status', 'type', 'is_checked', 'is_signing_at')
    list_filter = ('status', 'type', 'is_checked')
    search_fields = ('first_name', 'last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'lead', 'admin', 'lead_status', 'created_at')
    search_fields = ('lead__first_name', 'lead__last_name', 'comment')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state')
    list_filter = ('state',)
    search_fields = ('name',)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'university', 'education_type', 'grant', 'contract', 'evening', 'extramural')
    list_filter = ('education_type', 'grant', 'contract', 'evening', 'extramural')
    search_fields = ('name', 'university__name')


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'state', 'university', 'start_date', 'end_date', 'closed')
    list_filter = ('closed', 'state', 'university')
    search_fields = ('name',)


@admin.register(SeasonFacultyLimit)
class SeasonFacultyLimitAdmin(admin.ModelAdmin):
    list_display = ('id', 'season', 'faculty', 'grant', 'contract', 'evening', 'extramural')
    list_filter = ('season', 'faculty')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone_number', 'faculty', 'study_format', 'education_type')
    list_filter = ('faculty', 'education_type', 'study_format')
    search_fields = ('first_name', 'last_name', 'phone_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'type', 'amount', 'uploader_amount', 'is_payed')
    list_filter = ('type', 'is_payed')
    search_fields = ('student__first_name', 'student__last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CategoryOutlay)
class CategoryOutlayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'limit')
    search_fields = ('name',)


@admin.register(Outcome)
class OutcomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'amount', 'type', 'accountant')
    list_filter = ('type', 'category')
    search_fields = ('description',)
    readonly_fields = ('created_at', 'updated_at')