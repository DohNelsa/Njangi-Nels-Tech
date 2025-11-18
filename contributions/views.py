from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.db.models.functions import ExtractMonth
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Contribution, Withdrawal, TransactionLog
from .forms import ContributionForm, WithdrawalForm, WithdrawalApprovalForm
from members.models import Member
from calendar import month_name


@login_required
def contribution_list(request):
    """List all contributions"""
    contributions = Contribution.objects.all()
    
    # Filters
    member_filter = request.GET.get('member', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if member_filter:
        contributions = contributions.filter(member_id=member_filter)
    if date_from:
        contributions = contributions.filter(date__gte=date_from)
    if date_to:
        contributions = contributions.filter(date__lte=date_to)
    
    # Pagination
    paginator = Paginator(contributions, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total = contributions.aggregate(total=Sum('amount'))['total'] or 0
    category_totals_qs = contributions.values('category').annotate(total=Sum('amount'))
    category_summary = {
        key: 0 for key, _ in Contribution.CATEGORY_CHOICES
    }
    for item in category_totals_qs:
        category_summary[item['category']] = item['total'] or 0
    category_breakdown = [
        {
            'key': key,
            'label': label,
            'total': category_summary.get(key, 0)
        }
        for key, label in Contribution.CATEGORY_CHOICES
    ]

    expenses_qs = Withdrawal.objects.filter(status='approved')
    if member_filter:
        expenses_qs = expenses_qs.filter(member_id=member_filter)
    if date_from:
        expenses_qs = expenses_qs.filter(date__gte=date_from)
    if date_to:
        expenses_qs = expenses_qs.filter(date__lte=date_to)
    expenses_total = expenses_qs.aggregate(total=Sum('amount'))['total'] or 0
    net_total = total - expenses_total
    
    context = {
        'page_obj': page_obj,
        'members': Member.objects.filter(is_active=True),
        'member_filter': member_filter,
        'date_from': date_from,
        'date_to': date_to,
        'total': total,
        'category_breakdown': category_breakdown,
        'expenses_total': expenses_total,
        'net_total': net_total,
    }
    return render(request, 'contributions/contribution_list.html', context)


@login_required
def contribution_create(request):
    """Create new contribution"""
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can record contributions.')
        return redirect('contributions:list')
    
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            contribution = form.save(commit=False)
            contribution.created_by = request.user
            contribution.save()
            
            # Create transaction log
            TransactionLog.objects.create(
                transaction_type='contribution',
                member=contribution.member,
                amount=contribution.amount,
                description=f"Contribution: {contribution.description or 'No description'}",
                created_by=request.user,
                contribution=contribution
            )
            
            messages.success(request, 'Contribution recorded successfully!')
            return redirect('contributions:list')
    else:
        form = ContributionForm()
    
    return render(request, 'contributions/contribution_form.html', {'form': form})


@login_required
def account_balance(request, member_id):
    """View member account balance and history"""
    member = get_object_or_404(Member, pk=member_id)
    
    contributions = Contribution.objects.filter(member=member)
    withdrawals = Withdrawal.objects.filter(member=member)
    
    total_contributions = contributions.aggregate(total=Sum('amount'))['total'] or 0
    total_withdrawals = withdrawals.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_contributions - total_withdrawals
    
    context = {
        'member': member,
        'contributions': contributions[:20],
        'withdrawals': withdrawals[:20],
        'total_contributions': total_contributions,
        'total_withdrawals': total_withdrawals,
        'balance': balance,
    }
    return render(request, 'contributions/account_balance.html', context)


@login_required
def withdrawal_list(request):
    """List all withdrawals"""
    withdrawals = Withdrawal.objects.all()
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        withdrawals = withdrawals.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(withdrawals, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'contributions/withdrawal_list.html', context)


@login_required
def withdrawal_create(request):
    """Create withdrawal request"""
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.created_by = request.user
            withdrawal.save()
            
            # Create transaction log
            TransactionLog.objects.create(
                transaction_type='withdrawal',
                member=withdrawal.member,
                amount=withdrawal.amount,
                description=f"Withdrawal request: {withdrawal.reason}",
                created_by=request.user,
                withdrawal=withdrawal
            )
            
            messages.success(request, 'Withdrawal request submitted! Pending approval.')
            return redirect('contributions:withdrawal_list')
    else:
        form = WithdrawalForm()
    
    return render(request, 'contributions/withdrawal_form.html', {'form': form})


@login_required
def withdrawal_approve(request, pk):
    """Approve or reject withdrawal"""
    withdrawal = get_object_or_404(Withdrawal, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can approve withdrawals.')
        return redirect('contributions:withdrawal_list')
    
    if request.method == 'POST':
        form = WithdrawalApprovalForm(request.POST, instance=withdrawal)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            if withdrawal.status in ['approved', 'rejected']:
                withdrawal.approved_by = request.user
                withdrawal.approved_at = timezone.now()
            withdrawal.save()
            
            messages.success(request, f'Withdrawal {withdrawal.status} successfully!')
            return redirect('contributions:withdrawal_list')
    else:
        form = WithdrawalApprovalForm(instance=withdrawal)
    
    return render(request, 'contributions/withdrawal_approve.html', {'form': form, 'withdrawal': withdrawal})


@login_required
def transaction_logs(request):
    """View transaction logs"""
    logs = TransactionLog.objects.all()
    
    # Filters
    member_filter = request.GET.get('member', '')
    type_filter = request.GET.get('type', '')
    
    if member_filter:
        logs = logs.filter(member_id=member_filter)
    if type_filter:
        logs = logs.filter(transaction_type=type_filter)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'members': Member.objects.filter(is_active=True),
        'member_filter': member_filter,
        'type_filter': type_filter,
    }
    return render(request, 'contributions/transaction_logs.html', context)


@login_required
def yearly_statement(request):
    """Generate yearly account statement including automatic expense totals"""
    current_year = timezone.now().year
    try:
        year = int(request.GET.get('year', current_year))
    except (TypeError, ValueError):
        year = current_year

    contributions = Contribution.objects.filter(date__year=year)
    withdrawals = Withdrawal.objects.filter(status='approved', date__year=year)

    total_contributions = contributions.aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = withdrawals.aggregate(total=Sum('amount'))['total'] or 0
    net_total = total_contributions - total_expenses

    category_summary = {
        key: 0 for key, _ in Contribution.CATEGORY_CHOICES
    }
    for item in contributions.values('category').annotate(total=Sum('amount')):
        category_summary[item['category']] = item['total'] or 0
    category_breakdown = [
        {
            'key': key,
            'label': label,
            'total': category_summary.get(key, 0)
        }
        for key, label in Contribution.CATEGORY_CHOICES
    ]

    contribution_months = {
        entry['month']: entry['total'] or 0
        for entry in contributions.annotate(month=ExtractMonth('date')).values('month').annotate(total=Sum('amount'))
    }
    expense_months = {
        entry['month']: entry['total'] or 0
        for entry in withdrawals.annotate(month=ExtractMonth('date')).values('month').annotate(total=Sum('amount'))
    }

    monthly_breakdown = []
    for month_number in range(1, 13):
        contribution_amount = contribution_months.get(month_number, 0)
        expense_amount = expense_months.get(month_number, 0)
        monthly_breakdown.append({
            'month_label': month_name[month_number],
            'contributions': contribution_amount,
            'expenses': expense_amount,
            'net': contribution_amount - expense_amount,
        })

    contribution_years = {dt.year for dt in Contribution.objects.dates('date', 'year')}
    withdrawal_years = {dt.year for dt in Withdrawal.objects.dates('date', 'year')}
    year_options = sorted(contribution_years.union(withdrawal_years) or {current_year}, reverse=True)

    context = {
        'year': year,
        'year_options': year_options,
        'total_contributions': total_contributions,
        'total_expenses': total_expenses,
        'net_total': net_total,
        'category_breakdown': category_breakdown,
        'monthly_breakdown': monthly_breakdown,
    }
    return render(request, 'contributions/yearly_statement.html', context)


