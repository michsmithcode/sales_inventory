from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, StaffProfile



admin.site.register(CustomUser)

class CustomUserAdmin(UserAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        'middle_name',
        "role",
        "is_active",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "role",
                    "gender",
                    "phone_number",
                    "profile_picture",
                    "address",
                    "is_active_staff",
                )
            },
        ),
    )
    
admin.site.register(StaffProfile)

class StaffProfileAdmin(admin.ModelAdmin):

    list_display = (
        "employee_code",
        "user",
        "department",
        "hire_date",
    )

    search_fields = (
        "employee_code",
        "user__email",
        "user__first_name",
        "user__last_name",
    )