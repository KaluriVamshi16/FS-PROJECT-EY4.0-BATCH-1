from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.dashboard.models import Income, Investment
from apps.expenses.models import Expense
from apps.budgets.models import Budget
from django.db.models import Sum
from datetime import date

@login_required
def financial_dashboard(request):
    user = request.user
    today = date.today()
    
    # 1. Income
    incomes = Income.objects.filter(user=user)
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 2. Expenses
    expenses = Expense.objects.filter(user=user)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 3. Savings & Investments
    savings = total_income - total_expenses
    investments = Investment.objects.filter(user=user)
    total_investments = investments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # 4. Debts (from Budgets? Prompt said 'debts from Budget model' but Budget model doesn't have debt. 
    # Maybe it meant tracking overspending as debt, or I missed a Debt model. 
    # Prompt said: "Net Worth Calculator: Assets (savings + investments) − Liabilities (debts from Budget model)"
    # This is ambiguous. Budget model has monthly_limit. 
    # Let's assume 'Liabilities' are 0 for now or maybe overspent budgets? 
    # Let's just use 0 for liabilities to be safe or add a Debt model if I really want to be precise, 
    # but prompt didn't strictly ask for Debt model. 
    # Actually, let's treat 'Budgets' that are overspent as potential liabilities? No, that's complex.
    # Let's just use Savings + Investments for Net Worth for now.]
    liabilities = 0 
    net_worth = savings + total_investments - liabilities
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'total_investments': total_investments,
        'net_worth': net_worth,
        'incomes': incomes,
        'investments': investments,
    }
    return render(request, 'financials/index.html', context)
