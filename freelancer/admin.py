from django.contrib import admin
from freelancer.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from freelancer.forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

# Create new user form in the admin panel 
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Status)
admin.site.register(Service)
admin.site.register(Reviews)
admin.site.register(Project)
admin.site.register(Freelancer)
admin.site.register(Employer)