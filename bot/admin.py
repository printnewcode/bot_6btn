from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'is_paid', 'access_time_end', 'is_admin')
    search_fields = ('telegram_id', 'access_time_end')
    list_filter = ('is_admin','is_paid', 'access_time_end')


admin.site.register(User, UserAdmin)
