from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django import forms
from rocapi.models.user_profile import UserProfile
admin.site.register(UserProfile)
# User = get_user_model()
#
#
# class CustomUserModelForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'is_staff', 'first_name', 'last_name', 'mobile_no', 'user_type')
#
#
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'is_staff', 'first_name', 'last_name', 'mobile_no', 'user_type')
#     search_fields = ('mobile_no',)
#     form = CustomUserModelForm
#
#
# admin.site.register(User, CustomUserAdmin)


