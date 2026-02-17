from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

@login_required
def dashboard_view(request):
    try:
        from apps.budgets.utils import check_and_alert_budgets
        check_and_alert_budgets(request)
    except Exception as e:
        print(f"Error checking budget alerts: {e}")
        
    from apps.budgets.models import Budget
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'dashboard/index.html', {'budgets': budgets})
