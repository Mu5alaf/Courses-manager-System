from django.contrib import admin
from .models import (
    CustomUser,
    TrainerUser,
    Course,
    Enrollment,
    Payment,
)
# Register your models here.


#admin customization For CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_admin', 'is_trainer', 'created_at')
    search_fields = ('email',)
    list_filter = ('is_admin', 'is_trainer', 'created_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_trainer', 'is_active', 'is_staff')}),
    )

@admin.register(TrainerUser)
class TrainerUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'hourly_rate', 'joined_at')
    search_fields = ('user__email', 'phone_number')
    list_filter = ('hourly_rate', 'joined_at')
    autocomplete_fields = ['user']
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 1
    autocomplete_fields = ['trainer']
    
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price_type', 'price', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('price_type', 'created_by', 'created_at')
    inlines = [EnrollmentInline]
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by')
    
    
# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'course', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
    search_fields = ('trainer__user__email', 'course__title')
    date_hierarchy = 'payment_date'
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('trainer__user', 'course')

    def get_course_title(self, obj):
        return obj.course.title
    get_course_title.short_description = 'Course Title'

    def get_trainer_email(self, obj):
        return obj.trainer.user.email
    get_trainer_email.short_description = 'Trainer Email'