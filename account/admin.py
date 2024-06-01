from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import SRS
# from .models import ProjectTask
from .models import Employee
from django.utils.html import format_html
from .models import Client
# from .models import ProjectTask 
# from .models import Employee
from .models import AssignedTask

class UserAdmin(BaseUserAdmin):

    list_display = ('username', 'email', 'is_projectmanager', 'is_client', 'is_employee', 'approval_status')
    list_filter = ('is_projectmanager', 'is_client', 'is_employee', 'approval_status')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('is_projectmanager', 'is_client', 'is_employee', 'approval_status')}),  # Add your custom fields here
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Custom Fields', {'fields': ('is_projectmanager', 'is_client', 'is_employee', 'approval_status')}),
    )

admin.site.register(User, UserAdmin)

# class SRSAdmin(admin.ModelAdmin):
   
#     list_display = ('client_name', 'srs_document', 'upload_date')
#     search_fields = ('client_name',)
#     list_filter = ('upload_date',)
#     fields = ('client_name', 'srs_document', 'upload_date')
#     readonly_fields = ('upload_date',)
# admin.site.register(SRS, SRSAdmin)



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_email', 'approval_status')  # 'get_email' method ko yahan add kiya gaya hai
    search_fields = ['user__username', 'user__email']  # 'user__email' ko search_fields mein bhi add kiya gaya hai

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_email', 'company_name']  # Display username, email, and company name
    search_fields = ['user__username', 'user__email', 'company_name']  # Search by username, email, or company name

    def get_username(self, obj):
        return obj.user.username if obj.user else None
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email if obj.user else None
    get_email.short_description = 'Email'



    # Assumed your model is named ProjectTask
# from .models import ProjectTask  # Yahan apne model ka import statement sahi karein

# class ProjectTaskAdmin(admin.ModelAdmin):
#     list_display = ('project_name', 'manager', 'created_at')

    
#     def get_manager_username(self, obj):
#         return obj.manager.username
#     get_manager_username.short_description = 'Manager Username'  
    # Yahan par aap aur bhi configurations add kar sakte hain jaise list_filter, search_fields etc.

# admin.site.register(ProjectTask, ProjectTaskAdmin)

from .models import AssignedTask  # Adjust the import as necessary

@admin.register(AssignedTask)
class AssignedTaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'employee', 'assigned_at', 'srs_document_link')

    def srs_document_link(self, obj):
     if obj.srs_document:
        return format_html("<a href='{}'>Download</a>", obj.srs_document.srs_document.url)
     return "No document"
    srs_document_link.short_description = 'SRS Document'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "srs_document":
            kwargs["queryset"] = SRS.objects.filter(...) # Add your own filter criteria here
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
from .models import SRS
from django.contrib import admin

from .models import SRS
from django.contrib import admin

@admin.register(SRS)
class SRSAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_client_name', 'details')

    def get_client_name(self, obj):
        return obj.client.username if obj.client else None

    get_client_name.short_description = 'Client Name'


from django.contrib import admin
from .models import AmbiguityDetectionResult

admin.site.register(AmbiguityDetectionResult)
