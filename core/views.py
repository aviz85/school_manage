from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Course, Enrollment, Grade, Message
from django import forms
from django.core.exceptions import ObjectDoesNotExist
import uuid
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, EnrollmentSerializer, GradeSerializer, MessageSerializer

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

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Student, Teacher, Course

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()

    return Response({
        'totalStudents': total_students,
        'totalTeachers': total_teachers,
        'totalCourses': total_courses,
    })

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(recipient=user) | Q(sender=user))

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return Response({'unread_count': count})

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({'status': 'message marked as read'})

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sent(self, request):
        messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

# Keep your existing views if needed
# def add_student(request):
#     ...

# Create your views here.
