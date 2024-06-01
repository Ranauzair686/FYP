from django.urls import path
from .import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import pending_employee_approvals
from .views import simple_logout
from .views import index
from .views import submit_srs
from .views import client_srs_list_view
# from .views import upload_srs
from .views import view_issued_tasks
from .views import edit_task, view_task

from .views import delete_employee 
from .views import edit_employee  
from .views import employees_list 
from .views import assign_task  
from .views import upload_success
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [  
     path('download_reports/', views.download_reports_csv, name='download_reports_csv'),
     path('view_reports/', views.view_reports, name='view_reports'),   
     path('detect_ambiguity/', views.detect_ambiguity, name='detect_ambiguity'),
    #  path('detect_ambiguity/', views.detect_ambiguity_with_gpt4, name='detect_ambiguity'),
    path('employee_ambiguity_detection/', views.ambiguity_detection, name='employee_ambiguity_detection'),
    path('admin/', admin.site.urls),
    path('submit_srs/', submit_srs, name='upload_srs'),
    path('assigned-tasks/', views.view_assigned_tasks, name='assigned_tasks'),
    path('assign_task/', assign_task, name='assign_task'),
    path('employees/', employees_list, name='employees_list'),
    path('employee/delete/<int:pk>/', delete_employee, name='delete_employee'),
    path('employee/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
    path('employees/', views.employees_view, name='employees'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:task_id>/', view_task, name='view_task'),
    path('view_issued_tasks/', views.view_issued_tasks, name='view_issued_tasks'),
    path('add_project_task/', views.add_project_task, name='add_project_task'),
    path('success/', views.success, name='success_url'),
    # path('upload/', upload_srs, name='upload_srs'),
     path('upload_success/', upload_success, name='upload_success'),
    path('projectmanager/client-srs-list/', client_srs_list_view, name='client_srs_list'),
    path('success_url/', views.success, name='success'),
    path('pending-approvals/', pending_employee_approvals, name='pending_employee_approvals'),
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login'),
    path('', index, name='index'),
    path('login/', views.login_view, name='login_view'),

    path('register/', views.register, name='register'),
    path('projectmanager/', views.projectmanager, name='projectmanager'),
    path('client/', views.client, name='client'),
    path('employee/', views.employee, name='employee'),     
    path('client/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('employee/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('projectmanager/logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('projectmanager/logout/', simple_logout, name='logout'),
    path('employee/logout/', simple_logout, name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

