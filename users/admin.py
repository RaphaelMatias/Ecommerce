from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_customer')
    list_filter = ('is_active', 'is_staff', 'is_customer')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('first_name', 'last_name', 'username', 'birthday', 'address', 'phone_number')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer')}),
        ('Datas', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)