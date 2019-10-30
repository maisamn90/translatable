from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from freelancer.models import *
from freelancer.forms import *
from django.contrib.auth import authenticate, login as log_me_in, logout
from django.contrib.auth.hashers import make_password
from freelancer.filters import *
from django.db.models import Sum
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def index(request):
    reviews  = Reviews.objects.filter(is_active= True).order_by('-stars')
    top_two_reviews_list = []
    final_top_two_reviews_list = []
    top_two_freelancer = []
    
    for review in reviews:
        if review.freelancer not in top_two_freelancer:
            top_two_freelancer.append(review.freelancer)
            top_two_reviews_list.append(review)
            
    if len(top_two_reviews_list) > 2:
        for i in range(0,2):
            final_top_two_reviews_list.append(top_two_reviews_list[i])
    else:
        final_top_two_reviews_list = top_two_reviews_list
        
    status = get_object_or_404(Status, name="New")
    jobs_list = Project.objects.filter(is_active= True, status = status)
    
    top_two_jobs_list = []
    if len(jobs_list) < 2:
        top_two_jobs_list = jobs_list
    else:
        for i in range (0,2):
            top_two_jobs_list.append(jobs_list[i])
    
    for language in jobs_list:
        languges = language.language.all()
    
    # Get Jobs count by Service 
    translating_jobs_list = []
    writing_jobs_list = []
    expert_jobs_list = []
    proofreading_jobs_list = []
    for job in jobs_list:
        if job.service.id == 1:
            translating_jobs_list.append(job)
        elif job.service.id == 4:
            writing_jobs_list.append(job)
        elif job.service.id == 2:
            expert_jobs_list.append(job)
        elif job.service.id == 3:
            proofreading_jobs_list.append(job)
    
    translating_jobs = len(translating_jobs_list)
    writing_jobs = len(writing_jobs_list)
    expert_jobs = len(expert_jobs_list)
    proofreading_jobs = len(proofreading_jobs_list)
        
    
    return render(request, 'index.html' , {'jobs_list':jobs_list, 'translating_jobs':translating_jobs, 'writing_jobs':writing_jobs, 'languges':languges,
                                            'expert_jobs':expert_jobs,'proofreading_jobs':proofreading_jobs, 'top_two_jobs_list':top_two_jobs_list,
                                            'top_two_reviews_list':final_top_two_reviews_list,
                                            })

def search(request):
    status = get_object_or_404(Status, name="New")
    job_list = Project.objects.filter(is_active = True, status = status)
    job_filter = JobsFilter(request.GET, queryset=job_list)
    for language in job_list:
        languges = language.language.all()
    return render(request, 'find_jobs.html', {'filter': job_filter, 'languges':languges})

def search_freelancer(request):
    freelancer_list = Freelancer.objects.filter(is_active = True)
    freelancer_filter = FreelancersFilter(request.GET, queryset=freelancer_list)
    for lang in freelancer_list:
        languges = lang.language.all()
    print(languges, "lang")    
    return render(request, 'find_freelancer.html', {'freelancer_filter': freelancer_filter, 'languges':languges})

def signup_freelancer(request):
    if request.method == "POST":
        form = SignupFreelancerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_freelancer = True
            user.is_employer = False
            user.password=make_password(request.POST.get('password'))
            form.save()
            freelancer = Freelancer()
            freelancer.user = user
            freelancer.save()
            return redirect(login)
    else:
        form = SignupFreelancerForm()
    return render(request, 'signup_freelancer.html' , {'form':form})
    
def signup_employer(request):
    if request.method == "POST":
        form = SignupFreelancerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_freelancer = False
            user.is_employer = True
            user.password=make_password(request.POST.get('password'))
            form.save()
            employer = Employer()
            employer.user = user
            employer.save()
            return redirect(login)
    else:
        form = SignupFreelancerForm()
    return render(request, 'signup_employer.html' , {'form':form})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            print("correct")
            log_me_in(request,user)
            return redirect(index)
            
        else:
            return render(request, 'login.html' , {'error_msg':'error_login'})
    else:
        logout(request)
    
    return render(request, 'login.html')

def profile_freelancer(request):
    freelancer_user = request.user
    freelancer_profile = get_object_or_404(Freelancer, user=freelancer_user)
    try:
        reviews = Reviews.objects.filter(freelancer = freelancer_user)

    except Reviews.DoesNotExist:
        reviews = 0

    try:
        status = get_object_or_404(Status, id = 1)
        projects_worked = Project.objects.filter(freelancer = freelancer_user, status = status)
    except Project.DoesNotExist:
        projects_worked = {}
    
    try:
        status = get_object_or_404(Status, id = 2)
        projects_in_progress = Project.objects.filter(freelancer = freelancer_user, status = status)
    except Project.DoesNotExist:
        projects_in_progress = {}
        
    # get review percentage for freelancer
    stars_sum = 0
    total_stars = 0
    for i in reviews:
        stars_sum += i.stars
        total_stars += 5
    
    if total_stars:
        review_percentage = 100 * stars_sum / total_stars
    else:
        review_percentage = 0
        
    projects_worked_number = len(projects_worked)
    str_skills = freelancer_profile.skills
    if str_skills != None:
        if "," in str_skills:
            list_skills = str_skills.split(",")
        else:
            list_skills = [str_skills]
    else:
        list_skills= []
    
    print(freelancer_profile.language.all())
    return render(request, 'profile_freelancer.html' , {'freelancer_user':freelancer_user, 'freelancer_profile':freelancer_profile, 
                                                        'review':reviews, 'projects_number':projects_worked_number, 'list_skills':list_skills,
                                                        'languges':freelancer_profile.language.all(), 'edit':'edit', 'projects_worked':projects_worked,
                                                        'review_percentage':review_percentage, 'projects_in_progress':projects_in_progress,
                                                        })

def view_profile_freelancer(request,id):
    freelancer_user = get_object_or_404(CustomUser, pk=id)
    freelancer_profile = get_object_or_404(Freelancer, user=freelancer_user)
    try:
        reviews = Reviews.objects.filter(freelancer = freelancer_user)
    except Reviews.DoesNotExist:
        reviews = 0
    
    try:
        status = get_object_or_404(Status, name="Done")
        projects_worked = Project.objects.filter(freelancer = freelancer_user, status = status)
    except Project.DoesNotExist:
        projects_worked = {}
    
    # get review percentage for freelancer
    stars_sum = 0
    total_stars = 0
    for i in reviews:
        stars_sum += i.stars
        total_stars += 5
    
    if total_stars:
        review_percentage = 100 * stars_sum / total_stars
    else:
        review_percentage = 0
    
    projects_worked_number = len(projects_worked)
    str_skills = freelancer_profile.skills
    if str_skills != None:
        if "," in str_skills:
            list_skills = str_skills.split(",")
        else:
            list_skills = [str_skills]
    else:
        list_skills= []
    return render(request, 'profile_freelancer.html' , {'freelancer_user':freelancer_user, 'freelancer_profile':freelancer_profile, 
                                                        'review':reviews, 'projects_number':projects_worked_number, 'list_skills':list_skills,
                                                            'languges':freelancer_profile.language.all(), 'projects_worked':projects_worked,
                                                            'review_percentage':review_percentage
                                                        })
 
def edite_freelancer(request):
    freelancer_user = get_object_or_404(CustomUser, pk=request.user.id)
    freelancer_profile = get_object_or_404(Freelancer, user=freelancer_user)
    if request.method == "POST":
        form = EditeFreelancerUserForm(request.POST, request.FILES, instance = freelancer_user)
        form_profile = EditeFreelancerProfileForm(request.POST, request.FILES, instance = freelancer_profile)
        if form.is_valid():
            form.save()
            form_profile.save()
            return redirect (profile_freelancer)
    else:
        form = EditeFreelancerUserForm(instance = freelancer_user)
        form_profile = EditeFreelancerProfileForm(instance = freelancer_profile)
    
    return render(request, 'edite_freelancer.html', {'form':form, 'form_profile':form_profile})


def profile_employer(request):
    employer_user = request.user
    employer_profile = get_object_or_404(Employer, user = employer_user)
    employer_project = Project.objects.filter(is_active= True , employer = employer_user)
    
    in_progress_list = []
    done_list = []
    new_list = []
    
    new_msg =  True
    done_msg = True
    in_progress_msg = True
    for i in employer_project:
        if i.status.name == "In Progress":
            in_progress_list.append(i)
        elif i.status.name == "Done":
            done_list.append(i)
        elif i.status.name == "New":
            new_list.append(i)
    
    if len(in_progress_list) < 1:
        in_progress_msg = False
    
    if len(done_list) < 1:
        done_msg = False
        
    if len(new_list) < 1:
        new_msg = False
    
    # Delete and Complete job post        
    if request.method == "POST":
        if 'delete-btn' in request.POST:
            post_id = request.POST.get('post-id')
            post = get_object_or_404(Project, pk=post_id)
            post.is_active = False
            post.save()
            return redirect(profile_employer)
        else:
            post_id = request.POST.get('post-id')
            post = get_object_or_404(Project, pk=post_id)
            post_id = request.POST.get('post-id')
            post = get_object_or_404(Project, pk=post_id)
            review = Reviews()
            stars_review = request.POST.get('stars')
            desc_review = request.POST.get('review-description')
            post.status_id = 1
            post.completiondate = datetime.today()
            post.save()
            review.project = post
            review.freelancer = post.freelancer
            review.employer = post.employer
            review.stars = stars_review
            review.description = desc_review
            review.save()
            payment = get_object_or_404(Payments, project = post)
            payment.freelancer = post.freelancer
            payment.release_date = datetime.today()
            payment.save()
            return redirect(profile_employer)
            
    return render(request, 'profile_employer.html', {'employer_user':employer_user, 'employer_project':employer_project,
                                                    'new_msg':new_msg , 'done_msg':done_msg, 'in_progress_msg':in_progress_msg,
                                                    'employer_profile':employer_profile
                                                    })

def edite_employer(request):
    employer_user = get_object_or_404(CustomUser, pk=request.user.id)
    employer_profile = get_object_or_404(Employer, user = employer_user)
    if request.method == "POST":
        form_emp_user = EditeEmployerUserForm (request.POST, request.FILES, instance = employer_user)
        form_emp_profile = EditeEmployerprofileForm (request.POST, request.FILES, instance = employer_profile)
        if form_emp_user.is_valid() and form_emp_profile.is_valid():
            form_emp_user.save()
            form_emp_profile.save()
            return redirect (profile_employer)
            
    else:
        form_emp_user = EditeEmployerUserForm(instance = employer_user)
        form_emp_profile = EditeEmployerprofileForm (instance = employer_profile)
    return render(request, 'edite_employer.html', {'form_emp_user':form_emp_user, 'form_emp_profile':form_emp_profile})
    
def create_job(request):
    if request.method == "POST":
        form_add_job = AddJob(request.POST)
        if form_add_job.is_valid():
            jobb = form_add_job.save(commit=False)
            jobb.employer_user = request.user
            jobb.employer_id = request.user.id
            jobb.status = get_object_or_404(Status, name="New")
            form_add_job.save()
            return redirect(job_post_employer ,id=jobb.id)
    else:
        form_add_job = AddJob()
    return render(request, 'create_job.html'  , {'form_add_job':form_add_job})

def job_post_employer(request, id):
    apply_msg = False
    job_post = get_object_or_404(Project, pk=id)
    post_employer = get_object_or_404(Employer, user=job_post.employer) 
    CHECKOUT_SESSION_ID = request.session.session_key
    
    employer_posts_list = Project.objects.filter(is_active= True, employer_id = post_employer.user.id)
    employer_posts_count = len(employer_posts_list)
    str_skills = job_post.skills
    if str_skills != None:
        if "," in str_skills:
            list_skills = str_skills.split(",")
        else:
            list_skills = [str_skills]
    else:
        list_skills= []
    
    if request.user.is_freelancer == True:
        if request.method == "POST":
            freelancer = get_object_or_404(Freelancer, user = request.user)
            job_post.applied_freelancer.add(freelancer)
        
        if len(job_post.applied_freelancer.all()) > 0 :
            for freelancer_pro in job_post.applied_freelancer.all():
                freelancer = get_object_or_404(Freelancer, user = request.user)
                if freelancer_pro == freelancer:
                    apply_msg = True
                else:
                    apply_msg = False
                    
        return render(request, 'job_post_employer.html', {'job_post':job_post, 'languges':job_post.language.all(), 
                                                    'list_skills':list_skills, 'employer':post_employer,
                                                    'employer_posts_count':employer_posts_count,'freelancer_applied':job_post.applied_freelancer.all(),
                                                    'apply_msg':apply_msg})
    # submit buttons (Delete, complete , hire) button 
    if request.method == "POST":
        if 'delete-submit' in request.POST:
            post_id = request.POST.get('post-id')
            job_post = get_object_or_404(Project, pk=post_id)
            job_post.is_active = False
            job_post.save()
            return redirect(profile_employer)
        elif 'complete-submit' in request.POST:
            review = Reviews()
            stars_review = request.POST.get('stars')
            desc_review = request.POST.get('review-description')
            job_post.status_id = 1
            job_post.completiondate = datetime.today()
            job_post.save()
            review.project = job_post
            review.freelancer = job_post.freelancer
            review.employer = job_post.employer
            review.stars = stars_review
            review.description = desc_review
            review.save()
            payment = get_object_or_404(Payments, project = job_post)
            payment.freelancer = job_post.freelancer
            payment.release_date = datetime.today()
            payment.save()
            return redirect(profile_employer)
        else: #'hire-submit' in request.POST:
            freelancer_user_id = request.POST.get('freelancer-id')
            selected_freelancer = get_object_or_404(CustomUser, id = freelancer_user_id)
            charge = stripe.Charge.create(
            amount=job_post.budget * 100,
            currency='cad',
            description=('A payment of {} Charge from {} for {} ').format(job_post.budget , 
                                                                        post_employer.user.first_name,
                                                                        selected_freelancer.first_name
                                                                        ) ,
            source=request.POST['stripeToken']
                                        )   
            job_post.freelancer = selected_freelancer
            job_post.status_id = 2
            job_post.save()
            
            payment = Payments()
            payment.employer = post_employer.user
            payment.freelancer = selected_freelancer
            payment.project = job_post
            payment.description = ('A payment of {} Charge from {} for {} ').format(job_post.budget , 
                                                                        post_employer.user.first_name,
                                                                        selected_freelancer.first_name
                                                                        )
            payment.save()
        
        
        
    return render(request, 'job_post_employer.html', {'job_post':job_post, 'languges':job_post.language.all(), 
                                                    'list_skills':list_skills, 'employer':post_employer,
                                                    'employer_posts_count':employer_posts_count,'freelancer_applied':job_post.applied_freelancer.all(),
                                                    'CHECKOUT_SESSION_ID': CHECKOUT_SESSION_ID,
                                                        })

def signup_global(request):
    return render(request, 'signup_global.html')

def hire_freelancer(request):
    return render(request, 'hire_freelancer.html')

# Change user password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })

def success(request, session_id):
    return render(request, 'success.html')
    
def cancel(request):
    return render(request, 'cancel.html')

def employer_payment(request):
    user = request.user
    employer_payment = Payments.objects.filter(is_active= True, employer = user)
    print(employer_payment)
    return render(request, 'payment.html', {'employer_payment':employer_payment,'user':user})

def freelancer_payment(request):
    user = request.user
    freelancer_payment = Payments.objects.filter(is_active= True, freelancer = user)
    for i in freelancer_payment:
        print(i)
    return render(request, 'payment.html', {'freelancer_payment':freelancer_payment,'user':user})