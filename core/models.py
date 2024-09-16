from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Made optional
    date_of_birth = models.DateField()
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.student_id}"

class Teacher(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True, blank=True)
    subject = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = f"T-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.get_full_name()} - {self.subject}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(Student, through='Enrollment')

    def __str__(self):
        return f"{self.name} ({self.code})"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    grade = models.FloatField()
    date_graded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment.student} - {self.enrollment.course}: {self.grade}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.subject}"