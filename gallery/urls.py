from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_view, name='gallery'),
    path('upload/', views.media_upload, name='upload'),
    path('upload-media/', views.media_upload, name='upload_media'),  # Direct alias for admin access
    path('<int:pk>/edit/', views.media_edit, name='edit'),
    path('<int:pk>/delete/', views.media_delete, name='delete'),
]

