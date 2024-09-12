from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Student, Teacher, Course, Enrollment, Grade
from faker import Faker
import random
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create admin user
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
        UserProfile.objects.create(user=admin_user, user_type='ADMIN')

        # Create students
        for _ in range(50):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            profile = UserProfile.objects.create(user=user, user_type='STUDENT')
            Student.objects.create(
                user_profile=profile,
                student_id=fake.unique.random_number(digits=8),
                date_of_birth=fake.date_of_birth(minimum_age=6, maximum_age=18),
                grade=random.randint(1, 12)
            )

        # Create teachers
        subjects = ['Math', 'Science', 'English', 'History', 'Art', 'Music', 'Physical Education']
        for subject in subjects:
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password',
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            profile = UserProfile.objects.create(user=user, user_type='TEACHER')
            Teacher.objects.create(
                user_profile=profile,
                employee_id=fake.unique.random_number(digits=6),
                subject=subject
            )

        # Create courses
        teachers = Teacher.objects.all()
        for teacher in teachers:
            Course.objects.create(
                name=f"{teacher.subject} {random.randint(101, 999)}",
                code=fake.unique.random_number(digits=5),
                teacher=teacher
            )

        # Create enrollments and grades
        students = Student.objects.all()
        courses = Course.objects.all()
        for student in students:
            for course in random.sample(list(courses), k=random.randint(3, 5)):
                enrollment = Enrollment.objects.create(
                    student=student,
                    course=course,
                    date_enrolled=fake.date_between(start_date='-1y', end_date='today')
                )
                Grade.objects.create(
                    enrollment=enrollment,
                    grade=round(random.uniform(60, 100), 2),
                    date_graded=fake.date_between(start_date=enrollment.date_enrolled, end_date='today')
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))