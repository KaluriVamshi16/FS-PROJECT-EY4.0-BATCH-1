from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.core.models import FinancialHealthScore
from apps.core.score_engine import calculate_health_score
# Import necessary models for calculation
from apps.dashboard.models import Income
from apps.expenses.models import Expense
from apps.budgets.models import Budget
from apps.goals.models import FinancialGoal
from django.db.models import Sum

@login_required
def health_score_view(request):
    user = request.user
    
    # Fetch Data for Calculation
    monthly_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    savings = monthly_income - monthly_expenses
    
    budgets = Budget.objects.filter(user=user)
    total_budgets = budgets.count()
    budgets_exceeded = 0
    for b in budgets:
        if b.percentage_used > 100:
            budgets_exceeded += 1
            
    goals = FinancialGoal.objects.filter(user=user)
    goal_progress_sum = sum([g.progress_percentage for g in goals])
    goal_progress_avg = goal_progress_sum / goals.count() if goals.exists() else 0
    
    # Calculate Score
    health_data = calculate_health_score(
        user, monthly_income, monthly_expenses, savings, 
        total_budgets, budgets_exceeded, goal_progress_avg
    )
    
    context = {
        'score': health_data['total'],
        'grade': health_data['grade'],
        'tips': health_data['tips'],
        'savings': savings,
        'monthly_income': monthly_income,
        'savings_rate': (savings/monthly_income*100) if monthly_income > 0 else 0,
        'expense_ratio': (monthly_expenses/monthly_income*100) if monthly_income > 0 else 0,
    }
    
    return render(request, 'health/index.html', context)
