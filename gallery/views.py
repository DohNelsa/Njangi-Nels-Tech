from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import MediaFile
from .forms import MediaFileForm


def gallery_view(request):
    """Public gallery view - accessible to all users"""
    media_files = MediaFile.objects.filter(is_active=True)
    
    # Filter by type
    media_type = request.GET.get('type', '')
    if media_type:
        media_files = media_files.filter(media_type=media_type)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        media_files = media_files.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(media_files, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get counts for filter buttons
    total_count = MediaFile.objects.filter(is_active=True).count()
    image_count = MediaFile.objects.filter(is_active=True, media_type='image').count()
    video_count = MediaFile.objects.filter(is_active=True, media_type='video').count()
    
    context = {
        'page_obj': page_obj,
        'media_type': media_type,
        'search_query': search_query,
        'total_count': total_count,
        'image_count': image_count,
        'video_count': video_count,
    }
    return render(request, 'gallery/gallery.html', context)


@login_required
def media_upload(request):
    """Upload media files - admin only"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can upload media files.')
        return redirect('gallery:gallery')
    
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            media_file = form.save(commit=False)
            media_file.uploaded_by = request.user
            media_file.save()
            messages.success(request, f'{media_file.get_media_type_display()} uploaded successfully!')
            return redirect('gallery:gallery')
    else:
        form = MediaFileForm()
    
    return render(request, 'gallery/upload.html', {'form': form})


@login_required
def media_edit(request, pk):
    """Edit media file - admin only"""
    media_file = get_object_or_404(MediaFile, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can edit media files.')
        return redirect('gallery:gallery')
    
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media file updated successfully!')
            return redirect('gallery:gallery')
    else:
        form = MediaFileForm(instance=media_file)
    
    return render(request, 'gallery/upload.html', {'form': form, 'media_file': media_file})


@login_required
def media_delete(request, pk):
    """Delete media file - admin only"""
    media_file = get_object_or_404(MediaFile, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can delete media files.')
        return redirect('gallery:gallery')
    
    if request.method == 'POST':
        media_file.delete()
        messages.success(request, 'Media file deleted successfully!')
        return redirect('gallery:gallery')
    
    return render(request, 'gallery/delete.html', {'media_file': media_file})
