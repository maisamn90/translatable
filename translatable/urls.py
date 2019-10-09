"""translatable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from freelancer.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index),
    url(r'^jobs$', find_jobs),
    url(r'^freelancers$', find_freelancer),
    url(r'^signup_freelancer$', signup_freelancer),
    url(r'^signup_employer$', signup_employer),
    url(r'^login$', login),
    url(r'^profile_freelancer$', profile_freelancer),
    url(r'^job$', job_post),
    url(r'^edite_freelancer$', edite_freelancer),
    url(r'^edite_employer', edite_employer),
    url(r'^signup_global', signup_global),
    url(r'^create_job', create_job)
    
    
]
