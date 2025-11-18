from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Loan, LoanRepayment
from .forms import LoanForm, LoanApprovalForm, LoanRepaymentForm
from members.models import Member
from contributions.models import TransactionLog


@login_required
def loan_list(request):
    """List all loans"""
    loans = Loan.objects.all()
    
    # Filters
    status_filter = request.GET.get('status', '')
    member_filter = request.GET.get('member', '')
    
    if status_filter:
        loans = loans.filter(status=status_filter)
    if member_filter:
        loans = loans.filter(member_id=member_filter)
    
    # Pagination
    paginator = Paginator(loans, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'members': Member.objects.filter(is_active=True),
        'status_filter': status_filter,
        'member_filter': member_filter,
    }
    return render(request, 'loans/loan_list.html', context)


@login_required
def loan_detail(request, pk):
    """View loan details"""
    loan = get_object_or_404(Loan, pk=pk)
    repayments = LoanRepayment.objects.filter(loan=loan).order_by('-payment_date')
    
    context = {
        'loan': loan,
        'repayments': repayments,
        'total_paid': loan.get_paid_amount(),
        'remaining_balance': loan.get_remaining_balance(),
        'is_overdue': loan.is_overdue(),
    }
    return render(request, 'loans/loan_detail.html', context)


@login_required
def loan_create(request):
    """Create loan request"""
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.created_by = request.user
            loan.save()
            
            # Create transaction log
            TransactionLog.objects.create(
                transaction_type='loan_granted',
                member=loan.member,
                amount=loan.amount,
                description=f"Loan request: {loan.purpose}",
                created_by=request.user
            )
            
            messages.success(request, 'Loan request submitted! Pending approval.')
            return redirect('loans:list')
    else:
        form = LoanForm()
    
    return render(request, 'loans/loan_form.html', {'form': form})


@login_required
def loan_approve(request, pk):
    """Approve or reject loan"""
    loan = get_object_or_404(Loan, pk=pk)
    
    if not (request.user.is_staff or (hasattr(request.user, 'member_profile') and request.user.member_profile.is_admin())):
        messages.error(request, 'Only administrators can approve loans.')
        return redirect('loans:detail', pk=pk)
    
    if request.method == 'POST':
        form = LoanApprovalForm(request.POST, instance=loan)
        if form.is_valid():
            loan = form.save(commit=False)
            if loan.status == 'approved':
                loan.approved_by = request.user
                loan.approved_date = timezone.now().date()
                loan.status = 'active'
            elif loan.status == 'rejected':
                loan.approved_by = request.user
            loan.save()
            
            messages.success(request, f'Loan {loan.status} successfully!')
            return redirect('loans:detail', pk=pk)
    else:
        form = LoanApprovalForm(instance=loan)
    
    return render(request, 'loans/loan_approve.html', {'form': form, 'loan': loan})


@login_required
def repayment_create(request, loan_id=None):
    """Create loan repayment"""
    loan = None
    if loan_id:
        loan = get_object_or_404(Loan, pk=loan_id)
    
    if request.method == 'POST':
        form = LoanRepaymentForm(request.POST, loan=loan)
        if form.is_valid():
            repayment = form.save(commit=False)
            repayment.recorded_by = request.user
            repayment.status = 'completed'
            repayment.save()
            
            # Update loan status if fully paid
            if repayment.loan.get_remaining_balance() <= 0:
                repayment.loan.status = 'completed'
                repayment.loan.save()
            
            # Create transaction log
            TransactionLog.objects.create(
                transaction_type='loan_repayment',
                member=repayment.loan.member,
                amount=repayment.amount,
                description=f"Loan repayment: {repayment.notes or 'No notes'}",
                created_by=request.user
            )
            
            messages.success(request, 'Repayment recorded successfully!')
            return redirect('loans:detail', pk=repayment.loan.pk)
    else:
        form = LoanRepaymentForm(loan=loan)
    
    context = {
        'form': form,
        'loan': loan,
    }
    return render(request, 'loans/repayment_form.html', context)


