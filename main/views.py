from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Teacher
from .forms import LoginForm, StudentForm
from django.contrib import messages
import random

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(f"Attempting login for user: {user}")  # Debugging line
            if user is not None:
                login(request, user)
                request.session['teacher_id'] = user.id
                request.session['teacher_name'] = user.username
                return redirect('home')
            
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'teacher/login.html', {'form': form})

@login_required
def home(request):
    if not request.session.get('teacher_id'):
        return redirect('login')

    students = Student.objects.all()
    form = StudentForm()
    teacher_name = request.session.get('teacher_name', 'Guest')

    return render(request, 'teacher/home.html', {'students': students, 'form': form, 'teacher_name': teacher_name})
    
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            marks = form.cleaned_data['marks']

            student, created = Student.objects.get_or_create(
                name=name,
                subject=subject,
                defaults={'marks': marks}
            )
            

            if not created:
                student.marks += marks
                student.save()
    return redirect('home')

def edit_student(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)
    return render(request, 'teacher/edit_modal.html', {'form': form, 'student': student})

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()

        if not request.session.get('fp_user'):
            if user:
                request.session['fp_user'] = user.username
                return render(request, 'teacher/forgot_password.html', {'show_password_fields': True})
            else:
                return render(request, 'teacher/forgot_password.html', {'error': 'User not found'})
        else:
            old = request.POST.get('old_password')
            new = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')

            user = User.objects.get(username=request.session['fp_user'])

            if not user.check_password(old):
                return render(request, 'teacher/forgot_password.html', {
                    'show_password_fields': True, 'error': 'Old password incorrect'
                })

            if new != confirm:
                return render(request, 'teacher/forgot_password.html', {
                    'show_password_fields': True, 'error': 'Passwords do not match'
                })

            user.set_password(new)
            user.save()
            del request.session['fp_user']
            messages.success(request, "Password updated successfully. Please login.")
            return redirect('login')

    return render(request, 'teacher/forgot_password.html')

def delete_student(request, id):
    Student.objects.filter(id=id).delete()
    return redirect('home')

def logout_view(request):
    request.session.flush()
    return redirect('login')
