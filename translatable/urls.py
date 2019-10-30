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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name="index"),
    url(r'^jobs$', search, name="jobs"),
    url(r'^freelancers$', search_freelancer , name="freelancers"),
    url(r'^signup_freelancer$', signup_freelancer , name="signup_freelancer"),
    url(r'^signup_employer$', signup_employer , name="signup_employer"),
    url(r'^login$', login , name="login"),
    url(r'^profile_freelancer$', profile_freelancer, name="profile_freelancer"),
    url(r'^view_profile_freelancer/(?P<id>\d+)', view_profile_freelancer, name="view_profile_freelancer"),
    # url(r'^job$', job_post , name="job"),
    url(r'edite_freelancer$', edite_freelancer),
    url(r'^edite_employer$', edite_employer),
    url(r'^signup_global$', signup_global , name="signup_global"),
    url(r'^create_job$', create_job, name="create_job"),
    url(r'^job/(?P<id>\d+)', job_post_employer, name="job"),
    url(r'^profile_employer', profile_employer, name="profile_employer"),
    url(r'^hire_freelancer', hire_freelancer, name="hire_freelancer"),
    url(r'^password$', change_password, name='change_password'),
    url(r'^success/(?P<session_id>[\w\-]+)', success, name='success'),
    url(r'^cancel$', cancel, name='cancel'),
    url(r'^employer_payment', employer_payment, name='employer_payment'),
    url(r'^freelancer_payment$', freelancer_payment, name='freelancer_payment'),
    
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
