from django.contrib import admin
from .models import Profile
from django.contrib import auth

class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'email', 'phone', 'active', 'staff', 'admin', 'email_verified', 'phone_verified')
    list_filter = ('active', 'staff', 'admin', 'email_verified', 'phone_verified')

class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = ('__str__', 'first_name', 'last_name')

# Register your models here.
User = auth.get_user_model()
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(auth.models.Group)
