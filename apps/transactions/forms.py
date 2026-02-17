from django import forms
from apps.expenses.models import ExpenseCategory
from django.utils import timezone

class AddTransactionForm(forms.Form):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    type = forms.ChoiceField(choices=TRANSACTION_TYPES, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_type'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_date'}), initial=timezone.now)
    amount = forms.DecimalField(max_digits=12, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount', 'id': 'id_amount'}))
    description = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description', 'id': 'id_description'}))
    
    # Context specific fields
    expense_category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.none(), 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_expense_category'}),
        label="Category"
    )
    income_source = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Salary, Freelance', 'id': 'id_income_source'}),
        label="Source"
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_category'].queryset = ExpenseCategory.objects.filter(user=user) | ExpenseCategory.objects.filter(user__isnull=True)
