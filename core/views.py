from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Course, Enrollment, Grade
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import uuid
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, EnrollmentSerializer, GradeSerializer

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

def is_admin(user):
    try:
        return user.userprofile.user_type == 'ADMIN'
    except ObjectDoesNotExist:
        UserProfile.objects.create(user=user, user_type='ADMIN')
        return True

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

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]

# Keep your existing views if needed
# def add_student(request):
#     ...

# Create your views here.
