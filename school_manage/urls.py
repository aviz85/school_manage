"""
URL configuration for school_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views
from django.views.generic import TemplateView
from django.views.static import serve
from core.views import get_statistics, test_openai, UserViewSet

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'teachers', views.TeacherViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'enrollments', views.EnrollmentViewSet)
router.register(r'grades', views.GradeViewSet)
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/statistics/', get_statistics, name='get_statistics'),
    # Add these new URL patterns for the messaging system
    path('api/messages/inbox/', views.MessageViewSet.as_view({'get': 'inbox'}), name='message-inbox'),
    path('api/messages/sent/', views.MessageViewSet.as_view({'get': 'sent'}), name='message-sent'),
    path('api/messages/<int:pk>/mark-as-read/', views.MessageViewSet.as_view({'post': 'mark_as_read'}), name='message-mark-as-read'),
    path('api/messages/verify/', views.MessageViewSet.as_view({'post': 'verify'}), name='verify-message'),
    
    # Serve index.html for any other routes
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
    
    # Add this new URL pattern for testing OpenAI API
    path('api/test-openai/', test_openai, name='test-openai'),
]
