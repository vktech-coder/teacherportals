from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Student, Teacher
from .forms import LoginForm, StudentForm
from django.contrib import messages
import random

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            teacher = Teacher.objects.get(username=username, password=password)
            request.session['teacher_id'] = teacher.id
            return redirect('home')
        except Teacher.DoesNotExist:
            messages.error(request, "Invalid credentials")

    return render(request, 'teacher/login.html')

def home(request):
    if not request.session.get('teacher_id'):
        return redirect('login')

    students = Student.objects.all()
    form = StudentForm()
    return render(request, 'teacher/home.html', {'students': students, 'form': form})
    

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
        if not request.session.get('reset_username'):
            # Step 1: Username verification
            username = request.POST.get('username')
            try:
                user = User.objects.get(username=username)
                request.session['reset_username'] = username
                return render(request, 'teacher/forgot_password.html', {'show_password_fields': True})
            except User.DoesNotExist:
                return render(request, 'teacher/forgot_password.html', {'error': 'Username not found.'})

        else:
            # Step 2: Password update
            username = request.session.get('reset_username')
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            try:
                user = User.objects.get(username=username)

                if not user.check_password(old_password):
                    return render(request, 'teacher/forgot_password.html', {
                        'show_password_fields': True,
                        'error': 'Old password does not match.'
                    })

                if new_password != confirm_password:
                    return render(request, 'teacher/forgot_password.html', {
                        'show_password_fields': True,
                        'error': 'New passwords do not match.'
                    })

                # Set new password securely
                user.set_password(new_password)
                user.save()

                # Clear session
                request.session.pop('reset_username', None)

                # Add success message and redirect
                messages.success(request, "Password updated successfully. Please login.")
                return redirect('login')

            except User.DoesNotExist:
                return render(request, 'teacher/forgot_password.html', {
                    'error': 'Session expired. Try again.'
                })

    return render(request, 'teacher/forgot_password.html')

def delete_student(request, id):
    Student.objects.filter(id=id).delete()
    return redirect('home')

def logout_view(request):
    request.session.flush()
    return redirect('login')
