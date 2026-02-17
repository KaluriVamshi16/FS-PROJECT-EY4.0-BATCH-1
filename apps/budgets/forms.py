from django import forms
from .models import Budget
from apps.expenses.models import ExpenseCategory

class BudgetForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Budget
        fields = ['category', 'monthly_limit', 'month']
        widgets = {
            'monthly_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Limit'}),
            'month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpenseCategory.objects.filter(user=user) | ExpenseCategory.objects.filter(user__isnull=True)
