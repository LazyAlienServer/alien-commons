from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()


@admin.register(User)
class ProfileAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_moderator')
    ordering = ('email',)
    search_fields = ('email', 'username')

    readonly_fields = ('date_joined', 'last_login')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'avatar')}),
        ('Permissions', {
            'fields': ('is_active', 'is_moderator', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    username_field = "username"
