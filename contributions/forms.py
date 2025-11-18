from django import forms
from .models import Contribution, Withdrawal
from members.models import Member


class ContributionForm(forms.ModelForm):
    """Form for recording contributions"""
    class Meta:
        model = Contribution
        fields = ['member', 'amount', 'date', 'category', 'description']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(is_active=True)


class WithdrawalForm(forms.ModelForm):
    """Form for withdrawal requests"""
    class Meta:
        model = Withdrawal
        fields = ['member', 'amount', 'date', 'reason']
        widgets = {
            'member': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(is_active=True)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        member = self.cleaned_data.get('member')
        
        if member and amount:
            balance = member.get_current_balance()
            if amount > balance:
                raise forms.ValidationError(
                    f'Withdrawal amount ({amount}) exceeds available balance ({balance})'
                )
        return amount


class WithdrawalApprovalForm(forms.ModelForm):
    """Form for approving/rejecting withdrawals"""
    class Meta:
        model = Withdrawal
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


