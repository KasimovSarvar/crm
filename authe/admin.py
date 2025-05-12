from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "password", "full_name", "role","phone_number", "status","lead_number", "login_time")
    list_display_links =  ("id", "username", "password", "full_name", "role","phone_number", "status","lead_number", "login_time")