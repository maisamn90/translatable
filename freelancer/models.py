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

# Service model
class Service (models.Model):
    name = models.CharField(max_length=50, null= False)
    description= models.CharField(max_length=100, null= True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)
    
# CustomeUser Model
class CustomUser(AbstractUser):
    country = models.ForeignKey(Country, null= True)
    image = models.CharField(max_length=50, null= True)
    is_freelancer = models.BooleanField(default= True)
    is_employer = models.BooleanField(default= False)
    

# Freelancer model
class Freelancer(models.Model):
    user = models.ForeignKey(CustomUser, null= False)
    language = models.ManyToManyField(Language, null= True)
    skills = models.TextField(null= True)
    gender = models.CharField(max_length=10, null= True)
    description= models.CharField(max_length=1000, null= True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)

# Employer model
class Employer (models.Model):
    user = models.ForeignKey(CustomUser, null= False)
    employer_type = models.ForeignKey(Employer_type, null= True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return (self.name)

# Project model
class Project (models.Model):
    freelancer = models.ForeignKey(CustomUser, null= True, related_name="freelancer_user")
    employer = models.ForeignKey(CustomUser, null= False, related_name="employer_user")
    service = models.ForeignKey(Service, null= False)
    status= models.ForeignKey(Status, null=False)
    language = models.ManyToManyField(Language, null= False)
    skills = models.TextField(null= True)
    budget = models.IntegerField(null= False)
    timeperiod  = models.IntegerField(null= False)
    postdate = models.DateField(default=datetime.now)
    completiondate = models.DateField(null= True)
    description= models.CharField(max_length=1000, null= True)
    is_active = models.BooleanField(default= True)
    
    def __str__(self):
        return (self.name)

# Reviews  model
class Reviews (models.Model):
    freelancer = models.ForeignKey(CustomUser, null= True, related_name="review_freelancer_user")
    employer = models.ForeignKey(CustomUser, null= False, related_name="review_employer_user")
    project = models.ForeignKey(Project, null= False)
    description = models.CharField(max_length=300, null= True)
    stars = models.IntegerField(null= False)
    is_active = models.BooleanField(default= True)
    
    def __str__(self):
        return (self.name)

    

    