from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Employer, JobSeeker, JobApplication, Job,CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        user_type = request.POST["user_type"]

        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        
        # Create Employer or JobSeeker Profile
        if user_type == "employer":
            Employer.objects.create(user=user, company_name="")  # Can be updated later
        else:
            JobSeeker.objects.create(user=user)

        login(request, user)
        return redirect("home")  # Redirect to job listings or dashboard

    return render(request, "register.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user_type = request.POST["user_type"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            
            # Redirect based on user type
            if user_type == "employer":
                if Employer.objects.filter(user=user).exists():
                    return redirect("employer_dashboard")
                else:
                    messages.error(request, "Invalid Employer account.")
            elif user_type == "jobseeker":
                if JobSeeker.objects.filter(user=user).exists():
                    return redirect("home")  # Job seeker homepage
                else:
                    messages.error(request, "Invalid Job Seeker account.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated and hasattr(request.user, 'employer'):
        return redirect('employer_dashboard')  # Redirect employers to their dashboard

    jobs = Job.objects.all()  # Job seekers see available jobs

    query = request.GET.get('query')
    location = request.GET.get('location')
    salary = request.GET.get('salary')

    if query:
        jobs = jobs.filter(title__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if salary:
        try:
            salary = float(salary)
            jobs = jobs.filter(salary__gte=salary)
        except ValueError:
            pass

    return render(request, 'home.html', {'jobs': jobs})


@login_required
def share_job(request):
    if not hasattr(request.user, 'employer'):
        return redirect('home')  # Only employers can access

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        employer = request.user.employer

        Job.objects.create(
            title=title,
            description=description,
            location=location,
            salary=salary,
            category=category,
            employer=employer,
            image=image
        )
        return redirect('employer_dashboard')

    return render(request, 'share_job.html')


@login_required
def apply(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if hasattr(request.user, 'employer'):
        return redirect('home')  # Employers can't apply for jobs

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        cover_letter = request.POST.get('cover_letter')

        application = JobApplication(
            job=job,
            user=request.user,
            name=name,
            email=email,
            cover_letter=cover_letter
        )
        application.save()

        messages.success(request, 'Your application has been submitted successfully!')

        return redirect('home')

    return render(request, 'apply.html', {'job': job})


@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'employer'):
        return redirect('home')  # Only employers can access

    employer = request.user.employer
    jobs = Job.objects.filter(employer=employer)
    applications = JobApplication.objects.filter(job__in=jobs)

    return render(request, 'employer_dashboard.html', {'jobs': jobs, 'applications': applications})
