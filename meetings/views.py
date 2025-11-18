from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Meeting, Attendance
from .forms import MeetingForm, AttendanceForm, BulkAttendanceForm
from members.models import Member


@login_required
def meeting_list(request):
    """List all meetings"""
    meetings = Meeting.objects.all()
    
    # Filters
    status_filter = request.GET.get('status', '')
    if status_filter == 'upcoming':
        meetings = meetings.filter(date__gte=timezone.now(), is_completed=False)
    elif status_filter == 'completed':
        meetings = meetings.filter(is_completed=True)
    elif status_filter == 'past':
        meetings = meetings.filter(date__lt=timezone.now(), is_completed=False)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        meetings = meetings.filter(
            Q(title__icontains=search_query) |
            Q(agenda__icontains=search_query) |
            Q(minutes__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(meetings, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'meetings/meeting_list.html', context)


@login_required
def meeting_detail(request, pk):
    """View meeting details"""
    meeting = get_object_or_404(Meeting, pk=pk)
    attendance = Attendance.objects.filter(meeting=meeting)
    
    context = {
        'meeting': meeting,
        'attendance': attendance,
        'present_count': attendance.filter(present=True).count(),
        'absent_count': attendance.filter(present=False).count(),
        'total_members': Member.objects.filter(is_active=True).count(),
    }
    return render(request, 'meetings/meeting_detail.html', context)


@login_required
def meeting_create(request):
    """Create new meeting"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can create meetings.')
        return redirect('meetings:list')
    
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            messages.success(request, 'Meeting created successfully!')
            return redirect('meetings:detail', pk=meeting.pk)
    else:
        form = MeetingForm()
    
    return render(request, 'meetings/meeting_form.html', {'form': form})


@login_required
def meeting_edit(request, pk):
    """Edit meeting"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can edit meetings.')
        return redirect('meetings:detail', pk=pk)
    
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully!')
            return redirect('meetings:detail', pk=pk)
    else:
        form = MeetingForm(instance=meeting)
    
    return render(request, 'meetings/meeting_form.html', {'form': form, 'meeting': meeting})


@login_required
def attendance_record(request, meeting_id):
    """Record attendance for a meeting"""
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can record attendance.')
        return redirect('meetings:detail', pk=meeting_id)
    
    # Get all active members
    all_members = Member.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = BulkAttendanceForm(request.POST)
        if form.is_valid():
            present_members = form.cleaned_data['present_members']
            notes = form.cleaned_data['notes']
            
            # Create or update attendance records
            for member in all_members:
                attendance, created = Attendance.objects.get_or_create(
                    meeting=meeting,
                    member=member,
                    defaults={
                        'present': member in present_members,
                        'recorded_by': request.user,
                        'notes': notes if member in present_members else ''
                    }
                )
                if not created:
                    attendance.present = member in present_members
                    attendance.recorded_by = request.user
                    if notes and member in present_members:
                        attendance.notes = notes
                    attendance.save()
            
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('meetings:detail', pk=meeting_id)
    else:
        # Pre-populate with existing attendance
        existing_attendance = Attendance.objects.filter(meeting=meeting, present=True)
        initial = {
            'present_members': [a.member for a in existing_attendance]
        }
        form = BulkAttendanceForm(initial=initial)
    
    context = {
        'form': form,
        'meeting': meeting,
        'all_members': all_members,
    }
    return render(request, 'meetings/attendance_record.html', context)


