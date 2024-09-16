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
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.login_view, name='login'),  # Make this the main page
    path('home/', core_views.home_view, name='home'),
    path('add_student/', core_views.add_student, name='add_student'),
    path('add_teacher/', core_views.add_teacher, name='add_teacher'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('inbox/', core_views.inbox, name='inbox'),
    path('send_message/', core_views.send_message, name='send_message'),
    path('view_message/<int:message_id>/', core_views.view_message, name='view_message'),
]
