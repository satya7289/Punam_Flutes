
from django import forms
from django.contrib import auth
from django.contrib import admin
from .models import UserQuery, BlockedDomain, VerifyMobileOTP


User = auth.get_user_model()


class CustomUserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=auth.models.Group.objects.all(), required=False)

    class Meta:
        models = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(CustomUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'username', 'email', 'phone', 'email_verified', 'phone_verified', 'active', 'staff', 'admin', 'id')
    list_filter = ('active', 'staff', 'admin', 'email_verified', 'phone_verified')
    search_fields = ('email', 'phone', )
    exclude = ('user_permissions', 'is_superuser')
    form = CustomUserForm


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    list_display = ('__str__', 'first_name', 'last_name', 'email_opt_in')
    list_filter = ('email_opt_in',)


class UserQueryAdmin(admin.ModelAdmin):
    search_fields = ('full_name', 'email', 'contact_number', 'country', 'subject')
    list_display = ('__str__', 'full_name', 'email', 'contact_number', 'country', 'subject', 'created_at')
    list_filter = ('subject',)


class BlockedDomainAdmin(admin.ModelAdmin):
    search_fields = ('domain',)
    list_display = ('__str__', 'domain', 'block_status', 'created_at', 'update_at')
    list_filter = ('block_status',)


admin.site.register(VerifyMobileOTP)
admin.site.register(User, UserAdmin)
admin.site.register(BlockedDomain, BlockedDomainAdmin)
# admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserQuery, UserQueryAdmin)
