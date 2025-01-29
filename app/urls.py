from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    #Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    #AdminDashboard
    path('admin/dashboard/', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin/course/', views.course_view, name='admin-course'),
    path('admin/course/<uuid:pk>/', views.course_details_view, name='course-details'),
    path('admin/course/<uuid:pk>/edit/', views.course_edit_view, name='course-edit'),
    path('admin/course/<uuid:pk>/delete/', views.course_delete_view, name='course-delete'),
    path('admin/trainers/', views.trainers_view, name='trainers-list'),
    path('admin/trainer/<uuid:pk>/', views.trainer_details_view, name='trainer-details'),
    path('admin/trainer/<uuid:pk>/delete', views.trainer_delete_view, name='trainer-delete'),
    path('admin/trainers/<uuid:pk>/assign/', views.assign_course_view, name='assign-courses'),
    path('admin/payments/', views.payment_list_view, name='payments-list'),
    path('admin/payments/<uuid:pk>/', views.payment_details_view, name='payments-details'),
    
    #TrainerDashboard
    path('trainer/dashboard/', views.trainer_dashboard_view, name='trainer-dashboard'),  
    path('trainer/profile/edit/', views.trainer_edit_view, name='profile-edit'),
    path('trainer/courses/', views.trainer_course_view, name='trainer-courses'),
    path('trainer/<uuid:pk>/course/', views.trainer_course_details_view, name='courses-details'),
    path('trainer/update-enrollment-status/<uuid:pk>/', views.update_enrollment_status_view, name='update-enrollment-status'),
    path('trainer/course/store/', views.course_store_view, name='course-store'),
    path('course/<uuid:pk>/payment/', views.payment_view, name='payment-view'),

]
