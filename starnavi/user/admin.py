from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    search_fields = ('email', 'nickname', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
