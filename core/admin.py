from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Student, Teacher, Course, Enrollment, Grade

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'student_id', 'grade')
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name', 'student_id')

    def get_full_name(self, obj):
        return obj.user_profile.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'employee_id', 'subject')
    search_fields = ('user_profile__user__first_name', 'user_profile__user__last_name', 'employee_id', 'subject')

    def get_full_name(self, obj):
        return obj.user_profile.user.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    search_fields = ('name', 'code', 'teacher__user_profile__user__first_name', 'teacher__user_profile__user__last_name')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    list_filter = ('course', 'date_enrolled')
    search_fields = ('student__user_profile__user__first_name', 'student__user_profile__user__last_name', 'course__name')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'get_course', 'grade', 'date_graded')
    list_filter = ('enrollment__course', 'date_graded')
    search_fields = ('enrollment__student__user_profile__user__first_name', 'enrollment__student__user_profile__user__last_name', 'enrollment__course__name')

    def get_student(self, obj):
        return obj.enrollment.student
    get_student.short_description = 'Student'

    def get_course(self, obj):
        return obj.enrollment.course
    get_course.short_description = 'Course'
