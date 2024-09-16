from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Message
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Student
        fields = ['date_of_birth', 'grade']

    def save(self, commit=True):
        student = super().save(commit=False)
        student.student_id = str(uuid.uuid4())[:8].upper()  # Generate a unique ID
        if commit:
            student.save()
        return student

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    subject = forms.CharField(max_length=100)

    class Meta:
        model = Teacher
        fields = ['subject']

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

def is_admin(user):
    try:
        return user.userprofile.user_type == 'ADMIN'
    except ObjectDoesNotExist:
        return False

@login_required
@user_passes_test(is_admin)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Create User
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Create UserProfile
            UserProfile.objects.create(user=user, user_type='STUDENT')
            
            # Create Student
            student = form.save(commit=False)
            student.user_profile = user.userprofile
            student.save()
            
            return redirect('admin_dashboard')  # You'll need to create this view
    else:
        form = StudentForm()
    
    return render(request, 'core/add_student.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('home')  # You'll need to create a home view
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

@login_required
def home_view(request):
    user_type = request.user.userprofile.user_type
    context = {
        'user_type': user_type,
    }
    return render(request, 'core/home.html', context)

@login_required
@user_passes_test(is_admin)
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            user_profile = UserProfile.objects.create(user=user, user_type='TEACHER')
            teacher = form.save(commit=False)
            teacher.user_profile = user_profile
            teacher.save()
            return redirect('home')
    else:
        form = TeacherForm()
    return render(request, 'core/add_teacher.html', {'form': form})

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'core/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'core/send_message.html', {'form': form})

@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'core/view_message.html', {'message': message})

# Create your views here.
