# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('share_job/', views.share_job, name='share_job'),
     path('job/<int:job_id>/apply/', views.apply, name='apply_for_job'),
]