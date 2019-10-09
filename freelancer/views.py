from django.shortcuts import render, HttpResponse, get_object_or_404, redirect


# Create your views here.

def index(request):
    return render(request, 'index.html')

def find_jobs(request):
    return render(request, 'find_jobs.html')
    
def find_freelancer(request):
    return render(request, 'find_freelancer.html')

def signup_freelancer(request):
    return render(request, 'signup_freelancer.html')
    
def signup_employer(request):
    return render(request, 'signup_employer.html')

def login(request):
    return render(request, 'login.html')

def profile_freelancer(request):
    return render(request, 'profile_freelancer.html')
    
def job_post(request):
    return render(request, 'job_post.html')
    
def edite_freelancer(request):
    return render(request, 'edite_freelancer.html')
    
def edite_employer(request):
    return render(request, 'edite_employer.html')

def signup_global(request):
    return render(request, 'signup_global.html')
    
def create_job(request):
    return render(request, 'create_job.html')