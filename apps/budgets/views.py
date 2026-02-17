from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Budget
from .forms import BudgetForm

@login_required
def budget_list(request):
    from .utils import check_and_alert_budgets
    check_and_alert_budgets(request)
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budgets/index.html', {'budgets': budgets})

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            # Ensure month is first of month
            budget.month = budget.month.replace(day=1)
            budget.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(user=request.user)
    
    return render(request, 'budgets/add_budget.html', {'form': form})
