from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.expenses.models import Expense, ExpenseCategory
from apps.budgets.models import Budget
from apps.goals.models import FinancialGoal
from apps.dashboard.models import Income, Investment
from apps.chatbot.models import ChatMessage

@login_required
def settings_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'clear_data':
            # clear all user data
            Expense.objects.filter(user=request.user).delete()
            Budget.objects.filter(user=request.user).delete()
            FinancialGoal.objects.filter(user=request.user).delete()
            Income.objects.filter(user=request.user).delete()
            Investment.objects.filter(user=request.user).delete()
            ChatMessage.objects.filter(user=request.user).delete()
            messages.success(request, 'All data reset successfully.')
        elif action == 'toggle_theme':
            # Handle theme via cookie/session in frontend or here
            pass
            
    return render(request, 'settings/index.html')
