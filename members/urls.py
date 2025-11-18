from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.member_list, name='list'),
    path('<int:pk>/', views.member_detail, name='detail'),
    path('create/', views.member_create, name='create'),
    path('<int:pk>/edit/', views.member_edit, name='edit'),
    path('register/', views.register, name='register'),
    path('notify/', views.group_email, name='group_email'),
]


