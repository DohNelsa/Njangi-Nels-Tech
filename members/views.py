from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Member
from .forms import MemberForm, UserRegistrationForm, GroupEmailForm
from .emails import send_group_notification_email


@login_required
def member_list(request):
    """List all members"""
    members = Member.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Filter by role
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role=role_filter)
    
    # Pagination
    paginator = Paginator(members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'role_filter': role_filter,
    }
    return render(request, 'members/member_list.html', context)


@login_required
def member_detail(request, pk):
    """View member details"""
    member = get_object_or_404(Member, pk=pk)
    context = {
        'member': member,
    }
    return render(request, 'members/member_detail.html', context)


@login_required
def member_create(request):
    """Create new member"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can create members.')
        return redirect('members:list')
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member created successfully!')
            return redirect('members:list')
    else:
        form = MemberForm()
    
    return render(request, 'members/member_form.html', {'form': form})


@login_required
def member_edit(request, pk):
    """Edit member"""
    member = get_object_or_404(Member, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can edit members.')
        return redirect('members:detail', pk=pk)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully!')
            return redirect('members:detail', pk=pk)
    else:
        form = MemberForm(instance=member)
    
    return render(request, 'members/member_form.html', {'form': form, 'member': member})


def register(request):
    """User registration with automatic member profile creation"""
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('members:list')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create user account but keep inactive until admin approval
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.is_active = False
            user.save()
            
            # Create member profile marked as inactive/pending
            Member.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data.get('phone', ''),
                email=form.cleaned_data['email'],
                address=form.cleaned_data.get('address', ''),
                role='member',  # Default role
                is_active=False
            )
            
            messages.success(
                request,
                'Registration submitted successfully! An administrator will review your account shortly. '
                'You will receive access once your membership is approved.'
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'members/register.html', {'form': form})


@login_required
def group_email(request):
    """Allow administrators to send a group email notification to members."""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can send group notifications.')
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = GroupEmailForm(request.POST)
        if form.is_valid():
            selected_members = list(form.cleaned_data['recipients'])
            include_pending = form.cleaned_data['include_pending']

            if not selected_members:
                selected_members = list(Member.objects.filter(is_active=True))

            if include_pending:
                pending_members = Member.objects.filter(is_active=False)
                existing_ids = {member.pk for member in selected_members}
                for member in pending_members:
                    if member.pk not in existing_ids:
                        selected_members.append(member)
                        existing_ids.add(member.pk)

            if not selected_members:
                messages.error(request, 'No members available to receive the email.')
            else:
                sent_count = send_group_notification_email(
                    subject=form.cleaned_data['subject'],
                    message=form.cleaned_data['message'],
                    members=selected_members,
                )
                if sent_count > 0:
                    messages.success(request, f'Email sent to {sent_count} member(s).')
                    return redirect('members:list')
                messages.warning(request, 'No emails were sent. Please verify recipients have valid email addresses.')
    else:
        form = GroupEmailForm()

    return render(request, 'members/group_email_form.html', {'form': form})

