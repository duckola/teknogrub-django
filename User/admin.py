from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Users, Role


# 1. Custom Form for Adding User (Minimal Fields for Initial Save)
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('id_number', 'school_email', 'first_name', 'last_name', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_unusable_password()
        if commit:
            user.save()
        return user


# 2. Custom Form for EDITING an existing user (Shows Password Fields for Change)
class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label="Password", required=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Password confirmation", required=False, widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ('id_number', 'first_name', 'last_name', 'school_email', 'phone', 'role', 'password',
                  'password_confirm')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            raise forms.ValidationError("The two password fields did not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get("password"):
            user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


# 3. Main Admin Class (Final)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    def display_school_email(self, obj):
        return obj.school_email if obj.school_email else "-"

    display_school_email.short_description = 'SCHOOL EMAIL'

    list_display = ('id_number', 'display_school_email', 'first_name', 'last_name', 'role', 'is_staff')

    fieldsets = (
        ('Credentials', {'fields': ('id_number', 'password', 'password_confirm')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'school_email', 'phone')}),
        ('Access', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Groups/Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('id_number', 'school_email', 'first_name', 'last_name', 'role')}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if change:
            password = form.cleaned_data.get('password')
            if password:
                obj.set_password(password)

        super().save_model(request, obj, form, change)


admin.site.register(Role)
admin.site.register(Users, CustomUserAdmin)