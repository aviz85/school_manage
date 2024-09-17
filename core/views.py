from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Student, Teacher, Course, Enrollment, Grade, Message
from .serializers import StudentSerializer, TeacherSerializer, CourseSerializer, EnrollmentSerializer, GradeSerializer, MessageSerializer
from django import forms
import uuid
from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user, is_read=False)

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

    @action(detail=False, methods=['post'])
    def verify(self, request):
        content = request.data.get('content', '')
        
        prompt = f"""
        As an AI assistant for a school messaging system, your task is to verify if the following message adheres to school rules and is appropriate for communication within an educational setting. The message should be respectful, non-offensive, and relevant to school-related matters.

        Please analyze the following message and respond with either "APPROVED" if the message is appropriate, or "REJECTED" along with a brief explanation if the message violates any school communication guidelines.

        Message to verify:
        "{content}"

        Response format:
        Status: [APPROVED/REJECTED]
        Explanation: [If rejected, provide a brief explanation]
        """

        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an AI assistant that verifies school messages for appropriateness."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            ai_response = response.choices[0].message.content.strip()
            logger.info(f"OpenAI API response: {ai_response}")
            
            message_status = "APPROVED" if "APPROVED" in ai_response else "REJECTED"
            explanation = ai_response.split("Explanation:")[1].strip() if "Explanation:" in ai_response else ""
            
            return Response({
                "status": message_status,
                "explanation": explanation
            })
        except Exception as e:
            logger.error(f"Error in verify_message: {str(e)}")
            return Response({
                "status": "ERROR",
                "explanation": f"An error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Keep your existing views if needed
# def add_student(request):
#     ...

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_openai(request):
    try:
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "user", "content": "Say 'Hello, World!'"}
            ]
        )
        return Response({"message": response.choices[0].message.content})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
