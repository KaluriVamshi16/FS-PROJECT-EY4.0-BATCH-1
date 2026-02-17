from django.db.models import Sum

def calculate_health_score(user):
    from apps.expenses.models import Expense
    from apps.dashboard.models import Income
    from apps.core.models import FinancialHealthScore
    
    # 1. Savings Rate (Income - Expenses) / Income
    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    savings_rate = 0
    if total_income > 0:
        savings = total_income - total_expenses
        savings_rate = (savings / total_income) * 100
    
    # Simple Logic (Refined in next step if needed, prompting 'score_engine' usage)
    score = 50 + (savings_rate * 0.5)
    score = min(100, max(0, int(score)))
    
    # Save History
    FinancialHealthScore.objects.create(user=user, score=score)
    return score

def get_financial_context(user):
    from apps.expenses.models import Expense
    from apps.dashboard.models import Income
    from apps.budgets.models import Budget
    from apps.goals.models import FinancialGoal
    from django.db.models import Sum

    total_income = Income.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Budget Context
    budgets = Budget.objects.filter(user=user)
    budget_count = budgets.count()
    exceeded_count = 0
    for b in budgets:
        if b.spent > float(b.monthly_limit):
            exceeded_count += 1
            
    # Goals Context
    goals = FinancialGoal.objects.filter(user=user)
    goal_list = [f"{g.title}: {g.progress_percentage}% complete (Target: ₹{g.target_amount})" for g in goals]
    
    # Recent Expenses
    recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:5]
    recent_list = [f"₹{e.amount} on {e.category.name if e.category else 'Misc'} ({e.date})" for e in recent_expenses]

    context = f"""
    FINANCIAL SUMMARY for {user.username}:
    - Monthly Income: ₹{total_income}
    - Monthly Expenses: ₹{total_expenses}
    - Net Savings: ₹{total_income - total_expenses}

    BUDGET STATUS:
    - Total Budgets: {budget_count}
    - Budgets Exceeded: {exceeded_count}

    SAVINGS GOALS:
    {chr(10).join(goal_list) if goal_list else "No active goals."}

    RECENT ACTIVITY:
    {chr(10).join(recent_list) if recent_list else "No recent expenses."}
    """
    return context
