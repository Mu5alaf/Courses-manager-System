#django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from . import forms
from . import models

User = get_user_model()

'''Auth'''
# Signup View
def signup_view(request):
    if request.method == 'POST':
        #get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        #basic validation
        if not all([first_name, last_name, email, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'auth/signup.html')

        #check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'auth/signup.html')

        #create user
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password), 
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('app:login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'auth/signup.html')

    return render(request, 'auth/signup.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Basic validation
        if not email or not password:
            messages.error(request, "Both email and password are required")
            return redirect('app:login')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)  # Sets session cookie
            if user.is_admin:
                return redirect('app:admin-dashboard')
            else:
                return redirect('app:trainer-dashboard')
        else:
            messages.error(request, "Invalid email or password")
    
    return render(request, 'auth/login.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('app:login')


'''Admin Dashboard'''
#anylatycis dashboard
@admin_required
def admin_dashboard(request):
    #dahboard anyltics
    users_count = models.CustomUser.objects.count()
    student_count = models.TrainerUser.objects.count()
    courses_count = models.Course.objects.count()
    payments_count = models.Payment.objects.count()
    context = {
        'users_count': users_count,
        'student_count': student_count,
        'courses_count': courses_count,
        'payments_count': payments_count,
    }
    return render(request, 'admin/dashboard.html', context)

#Create course
@admin_required
def course_view(request):
    courses = models.Course.objects.all()
    form = forms.CourseForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Course created successfully!')
                return redirect('app:admin-course')
            except Exception as e:
                messages.error(request, f'Error saving course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    context = {
        'courses': courses,
        'form': form,
    }
    return render(request, 'admin/courses.html', context)

#course details
@admin_required
def course_details(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    context = {
        'course':course
        }
    return render(request, 'admin/course_info.html', context)

#course delete
@admin_required
def course_delete(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f'Course "{course_title}" deleted successfully')
        return redirect('app:admin-course')
    messages.error(request, 'Invalid request method')
    return redirect('app:course-details', pk=pk)

#course edite
@admin_required
def course_edit(request, pk):
    try:
        course = models.Course.objects.get(pk=pk)
    except models.Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('app:admin-course')

    form = forms.CourseForm(request.POST, request.FILES, instance=course)
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Course updated successfully!')
                return redirect('app:admin-course')
            except Exception as e:
                messages.error(request, f'Error saving course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.CourseForm(instance=course)
    context = {
        'course': course, 
        'form': form,
    }
    return render(request, 'admin/course_edit.html', context)

'''Trainer Dashboard'''
@login_required
def trainer_dashboard(request):
    return render(request, 'trainer/base.html')

