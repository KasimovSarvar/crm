from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'role', 'status', 'phone_number')
    search_fields = ('username', 'full_name', 'phone_number')
    list_filter = ('role', 'status')