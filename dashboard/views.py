from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from members.models import Member
from contributions.models import Contribution, Withdrawal, TransactionLog
from meetings.models import Meeting, Attendance
from loans.models import Loan
from announcements.models import Announcement, CommunityUpdate
from gallery.models import MediaFile


@login_required
def dashboard_index(request):
    """Main dashboard view for admins"""
    # Check if user is admin
    is_admin = False
    if request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin()):
        is_admin = True
    
    # Total savings/contributions
    total_contributions = Contribution.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = Withdrawal.objects.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0
    total_savings = total_contributions - total_withdrawals
    
    # Active loans
    active_loans = Loan.objects.filter(status__in=['approved', 'active'])
    total_loaned = active_loans.aggregate(total=Sum('amount'))['total'] or 0
    
    # Member stats
    total_members = Member.objects.filter(is_active=True).count()
    new_members_this_month = Member.objects.filter(
        date_joined__month=timezone.now().month,
        date_joined__year=timezone.now().year
    ).count()
    
    # Upcoming meetings
    upcoming_meetings = Meeting.objects.filter(
        date__gte=timezone.now(),
        is_completed=False
    ).order_by('date')[:5]
    
    # Recent contributions
    recent_contributions = Contribution.objects.order_by('-date', '-created_at')[:10]
    
    # Pending approvals
    pending_withdrawals = Withdrawal.objects.filter(status='pending').count()
    pending_loans = Loan.objects.filter(status='pending').count()
    
    # Recent transactions
    recent_transactions = TransactionLog.objects.order_by('-created_at')[:10]
    
    # Recent announcements
    recent_announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    # Media gallery stats
    total_media = MediaFile.objects.filter(is_active=True).count()
    image_count = MediaFile.objects.filter(is_active=True, media_type='image').count()
    video_count = MediaFile.objects.filter(is_active=True, media_type='video').count()
    
    context = {
        'is_admin': is_admin,
        'total_savings': total_savings,
        'total_contributions': total_contributions,
        'total_withdrawals': total_withdrawals,
        'total_loaned': total_loaned,
        'total_members': total_members,
        'new_members_this_month': new_members_this_month,
        'upcoming_meetings': upcoming_meetings,
        'recent_contributions': recent_contributions,
        'pending_withdrawals': pending_withdrawals,
        'pending_loans': pending_loans,
        'recent_transactions': recent_transactions,
        'recent_announcements': recent_announcements,
        'active_loans_count': active_loans.count(),
        'total_media': total_media,
        'image_count': image_count,
        'video_count': video_count,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def admin_management(request):
    """Comprehensive admin management page"""
    # Check if user is admin
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can access this page.')
        return redirect('dashboard:index')
    
    # Get statistics
    total_members = Member.objects.filter(is_active=True).count()
    total_contributions = Contribution.objects.aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = Withdrawal.objects.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0
    total_savings = total_contributions - total_withdrawals
    active_loans = Loan.objects.filter(status__in=['approved', 'active']).count()
    pending_withdrawals = Withdrawal.objects.filter(status='pending').count()
    pending_loans = Loan.objects.filter(status='pending').count()
    upcoming_meetings = Meeting.objects.filter(date__gte=timezone.now(), is_completed=False).count()
    total_media = MediaFile.objects.filter(is_active=True).count()
    image_count = MediaFile.objects.filter(is_active=True, media_type='image').count()
    video_count = MediaFile.objects.filter(is_active=True, media_type='video').count()
    
    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'total_contributions': total_contributions,
        'total_withdrawals': total_withdrawals,
        'active_loans': active_loans,
        'pending_withdrawals': pending_withdrawals,
        'pending_loans': pending_loans,
        'upcoming_meetings': upcoming_meetings,
        'total_media': total_media,
        'image_count': image_count,
        'video_count': video_count,
    }
    return render(request, 'dashboard/admin_management.html', context)


@login_required
def member_dashboard(request):
    """Dashboard view for regular members"""
    if not hasattr(request.user, 'member_profile'):
        messages.error(request, 'Please complete your member profile.')
        return redirect('members:list')
    
    member = request.user.member_profile
    
    # Member's contributions
    total_contributions = member.get_total_contributions()
    balance = member.get_current_balance()
    
    # Member's loans
    member_loans = Loan.objects.filter(member=member)
    active_loans = member_loans.filter(status__in=['approved', 'active'])
    
    # Upcoming meetings
    upcoming_meetings = Meeting.objects.filter(
        date__gte=timezone.now(),
        is_completed=False
    ).order_by('date')[:5]
    
    # Recent announcements
    recent_announcements = Announcement.objects.filter(
        is_active=True,
        is_pinned=False
    ).order_by('-created_at')[:5]
    
    pinned_announcements = Announcement.objects.filter(
        is_active=True,
        is_pinned=True
    ).order_by('-created_at')
    
    context = {
        'member': member,
        'total_contributions': total_contributions,
        'balance': balance,
        'member_loans': member_loans[:5],
        'active_loans': active_loans,
        'upcoming_meetings': upcoming_meetings,
        'recent_announcements': recent_announcements,
        'pinned_announcements': pinned_announcements,
    }
    return render(request, 'dashboard/member_dashboard.html', context)
