from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Announcement, CommunityUpdate
from .forms import AnnouncementForm, CommunityUpdateForm


@login_required
def announcement_list(request):
    """List all announcements"""
    announcements = Announcement.objects.filter(is_active=True)
    
    # Filter out expired announcements
    announcements = [a for a in announcements if not a.is_expired()]
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        announcements = [a for a in announcements if search_query.lower() in a.title.lower() or search_query.lower() in a.content.lower()]
    
    # Pagination
    paginator = Paginator(announcements, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'announcements/announcement_list.html', context)


@login_required
def announcement_detail(request, pk):
    """View announcement details"""
    announcement = get_object_or_404(Announcement, pk=pk)
    context = {
        'announcement': announcement,
    }
    return render(request, 'announcements/announcement_detail.html', context)


@login_required
def announcement_create(request):
    """Create new announcement"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can create announcements.')
        return redirect('announcements:list')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('announcements:list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/announcement_form.html', {'form': form})


@login_required
def announcement_edit(request, pk):
    """Edit announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can edit announcements.')
        return redirect('announcements:detail', pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement updated successfully!')
            return redirect('announcements:detail', pk=pk)
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'announcements/announcement_form.html', {'form': form, 'announcement': announcement})


@login_required
def update_feed(request):
    """Community updates feed"""
    updates = CommunityUpdate.objects.filter(is_active=True)
    
    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter:
        updates = updates.filter(update_type=type_filter)
    
    # Pagination
    paginator = Paginator(updates, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'type_filter': type_filter,
    }
    return render(request, 'announcements/update_feed.html', context)


@login_required
def update_create(request):
    """Create new community update"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can create updates.')
        return redirect('announcements:feed')
    
    if request.method == 'POST':
        form = CommunityUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.created_by = request.user
            update.save()
            messages.success(request, 'Update created successfully!')
            return redirect('announcements:feed')
    else:
        form = CommunityUpdateForm()
    
    return render(request, 'announcements/update_form.html', {'form': form})


