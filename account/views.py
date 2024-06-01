from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponseRedirect
# from .forms import SRSForm
from .models import SRS
from .forms import ProjectTaskForm
from .models import ProjectTask
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee 
from .forms import EmployeeForm 
from django.urls import reverse
from django.views.decorators.http import require_POST
from .forms import AssignTaskForm 

from django.shortcuts import render
from .models import AssignedTask
from django.utils.timezone import now
from .models import AssignedTask  # Assume that you have an AssignedTask model defined
from datetime import datetime


from .models import User
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import  User
def simple_logout(request):
    logout(request)  # Log out the user
    return redirect('index') 


def is_project_manager(user):
    return user.is_authenticated and user.is_projectmanager

@login_required
@user_passes_test(is_project_manager)
def pending_employee_approvals(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            user.approval_status = 'Approved'
            user.save()
            messages.success(request, f"Employee {user.username} has been approved successfully.")  # Add success message
            return redirect('pending_employee_approvals')  # Redirect to the same page to refresh the list

    pending_employees = User.objects.filter(is_employee=True, approval_status='Pending')
    print(pending_employees) 
    return render(request, 'pending_approvals.html', {'pending_employees': pending_employees})


def index(request):
    return render(request, 'index.html')
def projectmanager(request):
    return render(request,'projectmanager.html')


def client(request):
    return render(request,'client.html')


def employee(request):
    return render(request,'employee.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_projectmanager:
                login(request, user)
                return redirect('projectmanager')
            elif user is not None and user.is_client:
                login(request, user)
                return redirect('client')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

# def upload_srs(request):
#     if request.method == 'POST':
#         form = SRSForm(request.POST, request.FILES)
#         if form.is_valid(): 
#             form.save()
#             return HttpResponseRedirect('/upload_success/')
#     else:
#         form = SRSForm()
#     return render(request, 'upload.html', {'form': form})

def upload_success(request):
    return render(request, 'upload_success.html')


from django.shortcuts import render, redirect
from .forms import SRSFormSet
from .models import SRS

def client_srs_list_view(request):
    if request.method == 'POST':
        formset = SRSFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and form.has_changed():
                    details = form.cleaned_data.get('details')
                    # Yahan aapko client ID milna chahiye form se, ya aap ise session se ya request se fetch karna hoga
                    client_id = form.cleaned_data.get('client')  # example ke taur par, actual implementation aapki requirement pe depend karegi
                    SRS.objects.create(details=details, client_id=client_id)
            return redirect('client_srs_list_view')
    else:
        formset = SRSFormSet()

    # Yahan 'select_related' ko use karke related 'User' ko prefetch kiya ja raha hai
    srs_records = SRS.objects.select_related('client').all()
    
    return render(request, 'client_srs_list.html', {
        'formset': formset,
        'srs_records': srs_records
    })



from django.shortcuts import render, redirect
from .forms import ProjectTaskForm

def add_project_task(request):
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, request.FILES)  # Note the addition of request.FILES
        if form.is_valid():
            project_task = form.save(commit=False)
            project_task.manager = request.user  # Assuming the user is the manager
            project_task.save()
            form.save_m2m()  # If there are many-to-many fields, save them after the main object

            # Redirect to a new URL:
            return redirect('success_url')  # 'success_url' is the name of the URL pattern for the success page
    else:
        form = ProjectTaskForm()
    
    return render(request, 'add_project_task.html', {'form': form})


# views.py

def success(request):
    # Yahan aap success message display kar sakte hain
    return render(request, 'success1.html', {'message': 'Your task has been submitted successfully!'})

def view_issued_tasks(request):
    context = {'issued_tasks': ProjectTask.objects.filter(manager=request.user)}
    tasks = ProjectTask.objects.all()  # Retrieve all tasks from the database
    return render(request, 'view_issued_tasks.html', {'tasks': tasks})


def edit_task(request, task_id):
    task = get_object_or_404(ProjectTask, pk=task_id)
    if request.method == 'POST':
        form = ProjectTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('url')  # Replace with a URL name where you want to redirect after saving
    else:
        form = ProjectTaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form})

def view_task(request, task_id):
    task = get_object_or_404(ProjectTask, pk=task_id)
    return render(request, 'view_task.html', {'task': task})

def employees_view(request):
    employees = Employee.objects.all()  # Sabhi employees ko get karega
    return render(request, 'employees_list.html', {'employees': employees})



def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)  # Employee ko pk se database se nikal lein
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)  # POST data ke saath form ko populate karein
        if form.is_valid():
            form.save()  # Agar form valid hai to save karein
            return redirect('employees_list')  # Redirect karein employees list page pe
    else:
        form = EmployeeForm(instance=employee)  # Agar GET request hai to form ko employee ke data se bhar ke dikhayein

    return render(request, 'edit_employee.html', {'form': form}) 



def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect(reverse('employees_list')) 


def employees_list(request):
    employees = Employee.objects.all()
    return render(request, 'employees_list.html', {'employees': employees})



def assign_task(request):
    if request.method == 'POST':
        form = AssignTaskForm(request.POST)
        if form.is_valid():
            # Before saving the AssignedTask, set the srs_document instance
            assigned_task = form.save(commit=False)
            assigned_task.srs_document = form.cleaned_data['srs_document']
            assigned_task.save()
            # Redirect to a success page
            return redirect('success_url')
    else:
        form = AssignTaskForm()
    return render(request, 'assign_task.html', {'form': form})


def view_assigned_tasks(request):
    # This will get all assigned tasks for the logged-in user with their tasks and associated SRS documents
    assigned_tasks = AssignedTask.objects.filter(employee=request.user).select_related('task', 'srs_document')
    for task in assigned_tasks:
     print(task.task.project_name, task.srs_document)
    

    # Now, you can pass these to your template context
    return render(request, 'assigned_tasks.html', {'assigned_tasks': assigned_tasks})


from django.shortcuts import redirect
from .forms import SRSFormSet
from .models import SRS
from django.contrib.auth.decorators import login_required
@login_required 
def submit_srs(request):
    if request.method == 'POST':
        formset = SRSFormSet(request.POST)
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    # Attach the client who is submitting the SRS
                    SRS.objects.create(client=request.user, details=form['details'])
            return redirect('upload_success')  # Redirect to the Django admin
    else:
        formset = SRSFormSet()

    return render(request, 'submit_srs.html', {'formset': formset})


def ambiguity_detection(request):
    return render(request, 'employee_ambiguity_detection.html')

# views.py

# from django.conf import settings
# # Import relevant modules
# import requests
# from django.http import JsonResponse
# from django.shortcuts import render

# from dotenv import load_dotenv
# import os
# import requests
# from django.http import JsonResponse
# from django.shortcuts import render

# # Load environment variables
# load_dotenv()

# def detect_ambiguity(request):
#     if request.method == 'POST':
#         ambiguous_text = request.POST.get('ambiguous_text', '')

#         # Set the actual Gemini API endpoint
#         api_url = "https://api.gemini.com/your_specific_endpoint"
#         api_key = os.getenv('AIzaSyC8lePjznpqQ0Od0qdn9I2UskwUcwTE-o0')

#         # Prepare the headers and payload
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#             'Content-Type': 'application/json'
#         }

#         payload = {'text': ambiguous_text}

#         try:
#             # Make the POST request
#             response = requests.post(api_url, headers=headers, json=payload)
#             response_data = response.json()

#             if response.status_code == 200:
#                 return JsonResponse(response_data)
#             else:
#                 return JsonResponse({
#                     'result': 'error',
#                     'reason': response_data.get('reason', 'Unknown Error'),
#                     'message': response_data.get('message', 'No further information provided.')
#                 }, status=response.status_code)

#         except requests.RequestException as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return render(request, 'employee_ambiguity_detection.html')
# views.py

from django.shortcuts import render
from django.http import HttpResponse
import re
from .models import AmbiguityDetectionResult

# List of homonyms to check for ambiguity
homonyms_list = {
        'bank': ['financial institution', 'side of a river'],
        'bat': ['flying mammal', 'baseball equipment'],
        'lead': ['metal', 'to guide'],
        'tear': ['rip', 'drop of liquid from eyes'],
        'fair': ['just, impartial', 'moderately good'],
        'right': ['correct', 'opposite of left'],
        'meat': ['animal flesh for food', 'the main part of something'],
        'seal': ['marine mammal', 'to close something securely'],
         'meat': ['animal flesh for food', 'the main part of something'],
        'seal': ['marine mammal', 'to close something securely'],
    'fine': ['satisfactory', 'a small penalty'],
    'dress': ['garment', 'to put on clothes'],
    'wind': ['air in motion', 'to coil something'],
    'well': ['in good health', 'a hole in the ground'],
    'left': ['departed', 'opposite of right'],
    'light': ['not heavy', 'having little darkness'],
    'live': ['having life', 'to exist'],
    'cast': ['to throw', 'a group of actors'],
    'right': ['correct', 'opposite of left'],  # Added duplicate for emphasis (homophone)
    'fair': ['just, impartial', 'moderately good'],  # Added duplicate for emphasis (homophone)
    'way': ['manner', 'path'],
    'band': ['group of musicians', 'elastic loop that holds something together'],
    'lie': ['to tell an untruth', 'to be in a reclining position'],
    'wave': ['a surge of water', 'to signal with the hand'],
    'can': ['metal container', 'to be able to'],
     'peace': ['absence of war or violence', 'a single piece of something'],
    'wait': ['to stay in a place until something happens', 'weight'],
    'pair': ['two of something', 'to repair'],
    'son': ['a male child', 'the sun'],
    'know': ['to have knowledge or information', 'to gnaw at something'],
    'flower': ['the blossom of a plant', 'flour (a powdery substance made from grain)'],
    'eye': ['the organ of sight', 'a hole for a needle or thread'],
    'sea': ['a large body of salt water', 'see (to perceive with the eyes)'],
    'way': ['manner, method', 'weigh (to measure the heaviness of something)'],
    'hear': ['to perceive sound', 'here (in this place)'],
    'bare': ['uncovered'],  # Added new homophones
    'bear': ['to carry'],
    'cell': ['a biological unit'],
    'sell': ['to exchange goods for money'],
    'cite': ['to quote a source'],
    'sight': ['the ability to see'],
    'site': ['a location'],
    'coarse': ['rough'],
    'course': ['a path of study'],
    'fare': ['money paid for a ride'],
    'heal': ['to make healthy'],
    'heel': ['the back part of the foot'],
    'hole': ['a hollow space'],
    'whole': ['complete'],
    'knight': ['a medieval warrior'],
    'night': ['the time between sunset and sunrise'],
    'left': ['departed'],
    'loft': ['a high upper floor'],
    'right': ['correct'],
    'write': ['to create written text']
   
    }

def detect_ambiguity(request):
    if request.method == 'POST':
        ambiguous_text = request.POST.get('ambiguous_text', '').lower()
        detected_homonyms = []

        # Check each homonym in the provided text
        for word, meanings in homonyms_list.items():
            if re.search(rf'\b{word}\b', ambiguous_text):
                detected_homonyms.append((word, meanings))

        # Convert the list to a readable string
        homonyms_str = "\n".join([f"Word: {word}, Meanings: {', '.join(meanings)}" for word, meanings in detected_homonyms])

        # Save the results to the database
        AmbiguityDetectionResult.objects.create(
            text=ambiguous_text,
            detected_homonyms=homonyms_str
        )

        # Pass the detected homonyms to the template
        context = {'detected_homonyms': detected_homonyms}
        return render(request, 'ambiguity_report.html', context)

    return render(request, 'ambiguity_detection.html')

# views.py
from django.shortcuts import render
from .models import AmbiguityDetectionResult  # Import the correct model

def view_reports(request):
    # Fetch all ambiguity detection results, ordered by creation date (newest first)
    results = AmbiguityDetectionResult.objects.all().order_by('-created_at')

    # Pass the results to the template
    return render(request, 'view_reports.html', {'results': results})
# views.py
import csv
from django.http import HttpResponse
from .models import AmbiguityDetectionResult

def download_reports_csv(request):
    # Create the HTTP response object with the correct CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ambiguity_detection_results.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Detection Time', 'Text Analyzed', 'Detected Homonyms'])

    # Fetch all results from the database
    results = AmbiguityDetectionResult.objects.all().order_by('-created_at')

    # Write each result as a row in the CSV
    for result in results:
        writer.writerow([
            result.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            result.text,
            result.detected_homonyms
        ])

    return response


