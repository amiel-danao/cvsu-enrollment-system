from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "is_active",
    )
    list_filter = (
        "is_active",
    )
    search_fields = ("email", )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    # inlines = []
    exclude = ("is_superuser", "last_login", "date_joined")

    fieldsets = (
        ("User Information", {"fields": ("email", )}),
        ("Permissions", {
         "fields": ("is_active", "is_staff", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            "User Information",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff"
                ),
            },
        ),
    )
