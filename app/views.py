'''
@Mu5alaf
'''
#django
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.db.models import Q
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
        #validation
        if not email or not password:
            messages.error(request, "Both email and password are required")
            return redirect('app:login')
        #authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  
            if user.is_admin:
                return redirect('app:admin-dashboard')
                        
            if not user.is_trainer:
                messages.error(request, "This account is not authorized as a trainer")
                return redirect('app:login')
            
            return redirect('app:trainer-dashboard')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('app:login') 
    return render(request, 'auth/login.html')


#logout
def logout_view(request):
    logout(request)
    return redirect('app:login')


'''Admin Dashboard'''
#anylatycis dashboard
@admin_required
def admin_dashboard_view(request):
    #dahboard anyltics
    users_count = models.CustomUser.objects.count()
    trainers_count = models.TrainerUser.objects.count()
    courses_count = models.Course.objects.count()
    payments_count = models.Payment.objects.count()
    context = {
        'users_count': users_count,
        'trainers_count': trainers_count,
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
            messages.error(request, 'Please Fill Form Correctly')
    context = {
        'courses': courses,
        'form': form,
    }
    return render(request, 'admin/courses.html', context)

#course details
@admin_required
def course_details_view(request, pk):
    course = get_object_or_404(models.Course, pk=pk)
    context = {
        'course':course
        }
    return render(request, 'admin/course_info.html', context)

#course delete
@admin_required
def course_delete_view(request, pk):
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
def course_edit_view(request, pk):
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

#trainers list
@admin_required
def trainers_view(request):
    query = request.GET.get('search','').lower()
    #search querey 
    trainers = models.TrainerUser.objects.select_related('user').filter(
    Q(user__first_name__icontains=query) | 
    Q(user__last_name__icontains=query) | 
    Q(user__email__icontains=query)
    )
    return render(request, 'admin/trainers.html', {'trainers': trainers})

#trainers details
@admin_required
def trainer_details_view(request,pk):
    trainer = get_object_or_404(models.TrainerUser,pk=pk)
    context = {
        'trainer':trainer
    }
    return render(request, 'admin/trainer_info.html', context)

#trainers delete
@admin_required
def trainer_delete_view(request, pk):
    trainer = get_object_or_404(models.TrainerUser, pk=pk)
    if request.method == 'POST':
        trainer_name = trainer.user.email
        trainer.user.delete()
        messages.success(request, f'User "{trainer_name}" deleted successfully')
        return redirect('app:trainers-list')
    messages.error(request, 'Invalid request method')
    return redirect('app:trainers-list', pk=pk)

#add_course to trainer
@admin_required
def assign_course_view(request,pk):
    trainer_assign = get_object_or_404(models.TrainerUser, pk=pk)
    if request.method == 'POST':
        form = forms.AssignCourseForm(request.POST)
        if form.is_valid():
            selected_courses = form.cleaned_data['courses']
            trainer_assign.courses.set(selected_courses) 
            return redirect('app:trainers-list')
    else:
        form = forms.AssignCourseForm(initial={'courses': trainer_assign.courses.all()})
    context = {
        'trainer_assign': trainer_assign,
        'form': form, 
    }
    return render(request, 'admin/assign_course.html', context)

#payment record
@admin_required
def payment_list_view(request):
    payment_record = models.Payment.objects.all()
    context = {
        'payment_record':payment_record,
    }
    return render(request, 'admin/payment.html',context)

#payment details
@admin_required
def payment_details_view(request,pk):
    payment = get_object_or_404(models.Payment, pk=pk)
    context = {
        'payment':payment
    }
    return render(request, 'admin/payment_info.html',context)

'''Trainer Dashboard'''
#trainer profile
@login_required
def trainer_dashboard_view(request):
    try:
        profile = request.user.trainer_profile
    except models.TrainerUser.DoesNotExist:
        #auto create profile if not exist
        profile = models.TrainerUser.objects.create(user=request.user)
    context = {'profile': profile}
    return render(request, 'trainer/profile.html', context)
#trainer edite profile
@login_required
def trainer_edit_view(request):
    trainer_profile = request.user.trainer_profile
    if request.method == 'POST':
        form = forms.TrainerEditForm(request.POST, instance=trainer_profile)
        if form.is_valid():
            form.save()
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.save()
            messages.success(request, 'Profile updated successfully')
        return redirect('app:trainer-dashboard')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = forms.TrainerEditForm(instance=trainer_profile, initial=initial_data)
    
    context = {'form': form}
    return render(request, 'trainer/edit_profile.html', context)
#trainer course view
@login_required
def trainer_course_view(request):
    trainer = request.user.trainer_profile
    #enrolled courses
    enrollments = models.Enrollment.objects.filter(trainer=trainer).select_related('course')
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'trainer/courses.html', context)
#trainer course details
@login_required
def trainer_course_details_view(request,pk):
    try:
        trainer = models.TrainerUser.objects.get(user=request.user)
    except models.TrainerUser.DoesNotExist:
        raise ValueError("TrainerUser instance not found for the current user.")
    course = get_object_or_404(models.Course, id=pk)
    enrollment = get_object_or_404(models.Enrollment, course=course, trainer=trainer)
    
    context = {
        'course': course,
        'enrollment': enrollment,
    }
    return render(request, 'trainer/course_info.html', context)
# trainer update status
@login_required
def update_enrollment_status_view(request, pk):
    if request.method == "POST":
        try:
            trainer = models.TrainerUser.objects.get(user=request.user)
        except models.TrainerUser.DoesNotExist:
            raise ValueError("TrainerUser instance not found for the current user.")
        enrollment = get_object_or_404(models.Enrollment, pk=pk, trainer=trainer)
        enrollment.status = models.Enrollment.Status.COMPLETED
        enrollment.save()
        messages.success(request, "Congratulations! The course is completed.")
        return redirect('app:courses-details', pk=enrollment.course.id)

    return redirect('app:courses-details', pk=pk)

#corse store ourchase
@login_required
def course_store_view(request):
    courses = models.Course.objects.all()
    trainer = models.TrainerUser.objects.get(user=request.user)
    context = {
        'courses': courses,
        'trainer': trainer,
    }
    return render(request, 'trainer/store.html', context)

@login_required
def payment_view(request, pk):
    course = get_object_or_404(models.Course, id=pk)    
    if course in request.user.trainer_profile.courses.all():
        messages.info(request, "You are already enrolled in this course.")
        return redirect('app:courses-details', pk=course.id)  
    
    if request.method == 'POST':
        amount = course.price if course.price_type == 'Paid' else 0.00
        #create a payment record
        payment = models.Payment(
            trainer=request.user.trainer_profile,
            course=course,
            amount=amount,
            payment_date=timezone.now(), 
            status=models.Payment.Status.PENDING,
            note=request.POST.get('note', '')
        )
        
        if course.price_type == 'Paid':
            payment.status = models.Payment.Status.PAID 
        else:
            payment.status = models.Payment.Status.PAID  
    
        payment.save()
        course.trainers.add(request.user.trainer_profile) 
        messages.success(request, "Payment successful! You are now enrolled in the course.")
        return redirect('app:courses-details', pk=course.id)
    context = {
        'course': course
    }
    return render(request, 'trainer/payment.html', context)


