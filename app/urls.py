from django.urls import path
from . import views


app_name = 'app'

urlpatterns = [
    #Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    #AdminDashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('admin/course/', views.course_view, name='admin-course'),
    path('admin/course/<uuid:pk>/', views.course_details, name='course-details'),
    path('admin/course/<uuid:pk>/edit/', views.course_edit, name='course-edit'),
    path('admin/course/<uuid:pk>/delete/', views.course_delete, name='course-delete'),
    
    #TrainerDashboard
    path('trainer/dashboard/', views.trainer_dashboard, name='trainer-dashboard'),  
]
