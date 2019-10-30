from django import forms
from freelancer.models import *
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# signUp freelancer form
class SignupFreelancerForm (forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= CustomUser
        fields = ('first_name', 'last_name','email','username','password')
    
    def clean(self):
        cleaned_data = super(SignupFreelancerForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )

#edit freelancer User information Form 
class EditeFreelancerUserForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','email','username', 'image', 'country')
    def __init__(self, *args, **kwargs):
        super(EditeFreelancerUserForm, self).__init__(*args, **kwargs)
        self.fields['country'].empty_label = " -- Select a country -- "
    

#edit freelancer User information Form 
class EditeFreelancerProfileForm (forms.ModelForm):
    class Meta:
        model = Freelancer
        fields = ('language', 'title','years_experience','skills', 'gender', 'description')
    def __init__(self, *args, **kwargs):
        super(EditeFreelancerProfileForm, self).__init__(*args, **kwargs)
        self.fields['skills'].help_text = "Separate the words with Commas: (Example1,Example2)"
        self.fields['gender'].empty_label = " -- Select gender -- "

#edit employer User information Form 
class EditeEmployerUserForm (forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email', 'username')

#edit employer profile information Form 
class EditeEmployerprofileForm (forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('employer_type',)
    def __init__(self, *args, **kwargs):
        super(EditeEmployerprofileForm, self).__init__(*args, **kwargs)
        self.fields['employer_type'].empty_label = " -- Select a type -- "

#Create job post
class AddJob (forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','service','language','skills', 'budget','timeperiod','description')
    def __init__(self, *args, **kwargs):
        super(AddJob, self).__init__(*args, **kwargs)
        self.fields['skills'].help_text = "Separate the words with Commas: (Example1,Example2)" 
        self.fields['budget'].help_text = "Add budget in Canadian Dollar"
        self.fields['timeperiod'].help_text = "Total hours of work"
        
        self.fields['service'].empty_label = " -- Select a Service -- "


# Creation User form update
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

# Editing User form update
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

