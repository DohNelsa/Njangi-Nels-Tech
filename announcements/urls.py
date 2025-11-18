from django.urls import path
from . import views

app_name = 'announcements'

urlpatterns = [
    path('', views.announcement_list, name='list'),
    path('<int:pk>/', views.announcement_detail, name='detail'),
    path('create/', views.announcement_create, name='create'),
    path('<int:pk>/edit/', views.announcement_edit, name='edit'),
    path('feed/', views.update_feed, name='feed'),
    path('feed/create/', views.update_create, name='update_create'),
]


