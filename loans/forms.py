from django import forms
from .models import Loan, LoanRepayment
from members.models import Member


class LoanForm(forms.ModelForm):
    """Form for creating loan requests"""
    class Meta:
        model = Loan
        fields = ['member', 'amount', 'interest_rate', 'purpose', 'requested_date', 'due_date', 'notes']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'interest_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()
        requested_date = cleaned_data.get('requested_date')
        due_date = cleaned_data.get('due_date')
        
        if requested_date and due_date and due_date <= requested_date:
            raise forms.ValidationError('Due date must be after requested date.')
        
        return cleaned_data


class LoanApprovalForm(forms.ModelForm):
    """Form for approving/rejecting loans"""
    class Meta:
        model = Loan
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LoanRepaymentForm(forms.ModelForm):
    """Form for recording loan repayments"""
    class Meta:
        model = LoanRepayment
        fields = ['loan', 'amount', 'payment_date', 'notes']
        widgets = {
            'loan': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        loan = kwargs.pop('loan', None)
        super().__init__(*args, **kwargs)
        if loan:
            self.fields['loan'].queryset = Loan.objects.filter(pk=loan.pk)
        else:
            self.fields['loan'].queryset = Loan.objects.filter(status__in=['approved', 'active'])

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        loan = self.cleaned_data.get('loan')
        
        if loan and amount:
            remaining = loan.get_remaining_balance()
            if amount > remaining:
                raise forms.ValidationError(
                    f'Repayment amount ({amount}) exceeds remaining balance ({remaining})'
                )
        return amount


