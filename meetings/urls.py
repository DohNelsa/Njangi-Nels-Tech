from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meeting_list, name='list'),
    path('<int:pk>/', views.meeting_detail, name='detail'),
    path('create/', views.meeting_create, name='create'),
    path('<int:pk>/edit/', views.meeting_edit, name='edit'),
    path('<int:meeting_id>/attendance/', views.attendance_record, name='attendance'),
]


