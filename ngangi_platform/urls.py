"""
URL configuration for ngangi_platform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from gallery import views as gallery_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('members/', include('members.urls')),
    path('contributions/', include('contributions.urls')),
    path('meetings/', include('meetings.urls')),
    path('announcements/', include('announcements.urls')),
    path('loans/', include('loans.urls')),
    path('gallery/', include('gallery.urls')),
    path('upload-media/', gallery_views.media_upload, name='upload_media'),  # Direct access for admins
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html', next_page='dashboard:index'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


