from rest_framework import serializers
from .models import Student, Teacher, Course, Enrollment, Grade, Message
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'user_profile', 'student_id', 'date_of_birth', 'grade']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user_profile', 'employee_id', 'subject']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'teacher', 'students']

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'date_enrolled']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'enrollment', 'grade', 'date_graded']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'recipient', 'subject', 'content', 'timestamp', 'is_read']
        read_only_fields = ['sender', 'sender_username', 'timestamp', 'is_read']

    def get_sender_username(self, obj):
        return obj.sender.username

    def validate_recipient(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("You cannot send a message to yourself.")
        return value

    def validate(self, data):
        if not data.get('subject'):
            raise serializers.ValidationError({"subject": "Subject cannot be empty."})
        if not data.get('content'):
            raise serializers.ValidationError({"content": "Content cannot be empty."})
        return data