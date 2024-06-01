from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Employee,Client
from django import forms
from .models import SRS
from .models import ProjectTask 
from .models import AssignedTask
from django import forms
from django.forms import formset_factory



class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )



class SignUpForm(UserCreationForm):
    # Your existing fields here

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_projectmanager', 'is_employee', 'is_client')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        # Check if the user is a client
        if user.is_client:
            user.approval_status = 'Approved' 
            # Automatically approve client registrations

            # Set employee registrations to 'Pending' for approval
        if user.is_employee:
            user.approval_status = 'Pending'

        if commit:
            user.save()
            # Check if the user is a client
            if user.is_client:
                # Client instance create karein yahan
                Client.objects.create(user=user, company_name="Enter Company Name Here")
            else:
                # Employee instance create karein yahan
                Employee.objects.create(user=user)

        return user

from django import forms

class SRSForm(forms.Form):
    details = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter SRS details here', 'class': 'textarea-srs'}),
        label='SRS'
    )

# Define the formset with the form above
SRSFormSet = formset_factory(SRSForm, extra=1)
        
class ProjectTaskForm(forms.ModelForm):
    # Yahan par aap SRS model se related SRS document select karne ke liye ek field add kar sakte hain
    srs_document = forms.ModelChoiceField(queryset=SRS.objects.all(), required=False)
    
    class Meta:
        model = ProjectTask
        fields = ['project_name', 'project_description', 'srs_document']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

       

class AssignTaskForm(forms.ModelForm):
    srs_document = forms.ModelChoiceField(queryset=SRS.objects.all(), required=False, label='SRS Document')
    class Meta:
        model = AssignedTask
        fields = ['task', 'employee', 'srs_document']
        


