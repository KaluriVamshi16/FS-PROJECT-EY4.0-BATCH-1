from django.db.models import Sum
from django.utils import timezone
from django.contrib import messages

def check_and_alert_budgets(request):
    from .models import Budget
    from apps.expenses.models import Expense
    from django.db.models import Sum

    if not request.user.is_authenticated:
        return

    user = request.user
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    budgets = Budget.objects.filter(user=user, month=month_start)
    
    for budget in budgets:
        # Calculate spent using the model property for consistency
        spent = budget.spent
        
        if budget.monthly_limit > 0:
            percent = (spent / float(budget.monthly_limit)) * 100
            
            if percent >= 80:
                if not budget.alert_sent:
                    messages.warning(request, f"⚠️ Alert: You have used {int(percent)}% of your {budget.category.name} budget!")
                    budget.alert_sent = True
                    budget.save()
