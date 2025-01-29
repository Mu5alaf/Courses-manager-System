import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from .utils import image_upload,video_upload

# Create your models here.


class UserModelManager(BaseUserManager):
    #baseUser
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email Must be Set')
        email = self.normalize_email(email).lower()
        extra_fields.setdefault('is_active', True) 
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #SuperUser
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_trainer', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    username = None 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserModelManager()
    
    def __str__(self):
        return self.email
    

class TrainerUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='trainer_profile')
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], null=True,blank=True,db_index=True)
    about_me = models.TextField(max_length=500, null=True,blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=0.00)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Trainer User"
        verbose_name_plural = "Trainer Users" 
    
    #get full name if is set else email
    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name if full_name.strip() else self.user.email

class Course(models.Model):
    class Status(models.TextChoices):
        FREE = 'Free'
        PAID = 'Paid'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=image_upload,null=True, blank=True)
    video = models.FileField(upload_to=video_upload,null=True, blank=True)
    price_type = models.CharField(max_length=25, choices=Status.choices, default=Status.PAID)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    total_hours = models.PositiveIntegerField(validators=[MinValueValidator(1)],default=1)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='courses_creator', db_index=True)
    trainers =  models.ManyToManyField(TrainerUser, through='Enrollment', related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses" 
    
    #Validation on Courses Pricing Type
    def clean(self):
        if self.price_type == Course.Status.PAID and self.price <= 0:
            raise ValidationError('Paid courses must have a price greater than 0')
        if self.price_type == Course.Status.FREE and self.price != 0:
            raise ValidationError('Free courses must have price set to 0')
        return super().clean()

    def __str__(self):
        return f"{self.title} ({self.get_price_type_display()})"


class Enrollment(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = 'In Progress'
        COMPLETED = 'Completed'
        ABANDONED = 'Abandoned'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,null=True)
    trainer = models.ForeignKey(TrainerUser, on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=25, choices=Status.choices , default=Status.IN_PROGRESS)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        #user canot have course twice
        unique_together = ('course', 'trainer')
        verbose_name_plural = "Enrollments" 
    
    def __str__(self):
        return f"{self.trainer} - {self.course} ({self.get_status_display()})"
    

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending'
        PAID = 'Paid'
        FAILED = 'Failed'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trainer = models.ForeignKey(TrainerUser, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    payment_date = models.DateField()
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.PENDING)
    note = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = "Payment"
        verbose_name_plural = "Payments" 
    
    #Vaildation the free course value to be only zero fees
    def clean(self):
        if self.course.price_type == Course.Status.FREE and self.amount !=0:
            raise ValidationError("Free courses must have a payment amount of 0.")
        return super().clean()
    
    #handel payment when course is free
    def save(self, *args, **kwargs):
        if self.course.price_type == Course.Status.FREE:
            self.amount = 0.00
            self.status = Payment.Status.PAID
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment {self.get_status_display()} - {self.amount}"