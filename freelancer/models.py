from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

# Country model
class Country(models.Model):
    name = models.CharField(max_length=50, null= False)
    description = models.CharField(max_length=100, null= True)
    is_active = models.BooleanField(default= True)
    

    def __str__(self):
        return (self.name)
        
# Language model
class Language (models.Model):
    name = models.CharField(max_length=50, null= False)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)
        
# Status model
class Status (models.Model):
    name = models.CharField(max_length=50, null= False)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)

# Employer type model
class Employer_type (models.Model):
    name = models.CharField(max_length=50, null= False)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)

# Gender type model
class Gender (models.Model):
    name = models.CharField(max_length=50, null= False)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)

# Service model
class Service (models.Model):
    name = models.CharField(max_length=50, null= False)
    description= models.CharField(max_length=100, null= True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)
    
# CustomeUser Model
class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, null= True,on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='profile_picture/', default='profile_picture/default_profile.png')
    is_freelancer = models.BooleanField(default= True)
    is_employer = models.BooleanField(default= False)
    

# Freelancer model
class Freelancer(models.Model):
    user = models.ForeignKey(CustomUser, null= False, on_delete=models.CASCADE,)
    language = models.ManyToManyField(Language, null= True, related_name="freelancer_language")
    gender = models.ForeignKey(Gender, null= True, on_delete=models.CASCADE,)
    title = models.CharField(max_length=100, null= True)
    years_experience = models.IntegerField(null= True)
    skills = models.CharField(max_length=300, null= True)
    description= models.TextField(max_length=1000, null= True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.user.username)

# Employer model
class Employer (models.Model):
    user = models.ForeignKey(CustomUser, null= False, on_delete=models.CASCADE,)
    employer_type = models.ForeignKey(Employer_type, null= True, on_delete=models.CASCADE,)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.user.first_name)

# Project model
class Project (models.Model):
    freelancer = models.ForeignKey(CustomUser, null= True, related_name="freelancer_user", on_delete=models.CASCADE,)
    employer = models.ForeignKey(CustomUser, null= False, related_name="employer_user", on_delete=models.CASCADE,)
    service = models.ForeignKey(Service, null= False, on_delete=models.CASCADE,)
    status= models.ForeignKey(Status, null=False, on_delete=models.CASCADE,)
    language = models.ManyToManyField(Language, null= False)
    name = models.CharField(max_length=100, null= False)
    skills = models.CharField(max_length=300, null= True)
    budget = models.IntegerField(null= False)
    timeperiod  = models.IntegerField(null= False)
    postdate = models.DateField(default=datetime.now)
    completiondate = models.DateField(null= True)
    description= models.TextField(max_length=1000, null= True)
    is_active = models.BooleanField(default= True)
    applied_freelancer = models.ManyToManyField(Freelancer, null= True)
    
    def __str__(self):
        return (self.name)

# Reviews  model
class Reviews (models.Model):
    freelancer = models.ForeignKey(CustomUser, null= True, related_name="review_freelancer_user", on_delete=models.CASCADE,)
    employer = models.ForeignKey(CustomUser, null= False, related_name="review_employer_user", on_delete=models.CASCADE,)
    project = models.ForeignKey(Project, null= False, on_delete=models.CASCADE,)
    description = models.CharField(max_length=300, null= True)
    stars = models.IntegerField(null= False)
    is_active = models.BooleanField(default= True)
    
    def __str__(self):
        return (self.freelancer.username)

# Payments  model
class Payments (models.Model):
    freelancer = models.ForeignKey(CustomUser, null= True, related_name="payment_freelancer_user", on_delete=models.CASCADE,)
    employer = models.ForeignKey(CustomUser, null= False, related_name="payment_employer_user", on_delete=models.CASCADE,)
    project = models.ForeignKey(Project, null= False, on_delete=models.CASCADE,)
    description = models.CharField(max_length=300, null= True)
    payment_date = models.DateField(default=datetime.now)
    release_date = models.DateField(null= True)
    is_active = models.BooleanField(default= True)
    
    def __str__(self):
        return (self.project.name)
    

    