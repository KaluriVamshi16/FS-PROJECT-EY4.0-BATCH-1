from django import forms
from .models import FinancialGoal

class FinancialGoalForm(forms.ModelForm):
    icon = forms.CharField(required=False, initial='🎯', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 🎯'}))

    class Meta:
        model = FinancialGoal
        fields = ['title', 'target_amount', 'target_date', 'icon', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Buy a Car'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target Amount'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Details...', 'rows': 3}),
        }
