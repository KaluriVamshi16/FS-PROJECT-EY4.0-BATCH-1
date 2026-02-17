import os
import django
from django.utils import timezone
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finsight.settings')
django.setup()

from apps.budgets.models import Budget
from apps.expenses.models import Expense, ExpenseCategory
from django.contrib.auth.models import User
from django.db.models import Sum

def verify_budget_logic():
    # 1. Setup - get or create user
    user = User.objects.first()
    if not user:
        user = User.objects.create_user(username='testuser', password='password')
    
    # 2. Setup - get or create category
    category, created = ExpenseCategory.objects.get_or_create(name='Food', user=user)
    if not created:
        category.user = user
        category.save()

    # 3. Create a budget for this month
    today = timezone.now().date()
    month_start = today.replace(day=1)
    
    # Clear existing budgets/expenses for clean test
    Budget.objects.filter(user=user, category=category, month=month_start).delete()
    Expense.objects.filter(user=user, category=category, date__gte=month_start).delete()

    budget = Budget.objects.create(
        user=user,
        category=category,
        monthly_limit=Decimal('1000.00'),
        month=month_start
    )
    
    print(f"Created budget: {budget}")
    print(f"Initial spent: {budget.spent}, initial % used: {budget.percentage_used}%")

    # 4. Add expense below 80%
    Expense.objects.create(
        user=user,
        amount=Decimal('500.00'),
        category=category,
        date=today
    )
    
    # Reload budget
    budget.refresh_from_db()
    print(f"After ₹500 expense - spent: {budget.spent}, % used: {budget.percentage_used}%")
    
    # 5. Add expense to reach > 80%
    Expense.objects.create(
        user=user,
        amount=Decimal('350.00'),
        category=category,
        date=today
    )
    
    # Reload budget
    budget.refresh_from_db()
    print(f"After total ₹850 expense - spent: {budget.spent}, % used: {budget.percentage_used}%")
    
    # 6. Test Alert Logic
    from apps.budgets.utils import check_and_alert_budgets
    from django.test import RequestFactory
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.contrib.sessions.middleware import SessionMiddleware

    factory = RequestFactory()
    request = factory.get('/')
    request.user = user
    
    # Add session manually for messages middleware
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    
    # Add messages middleware manually for testing
    storage = FallbackStorage(request)
    setattr(request, '_messages', storage)
    
    try:
        check_and_alert_budgets(request)
    except Exception as e:
        print(f"Alert check failed with error: {e}")
    
    budget.refresh_from_db()
    print(f"Alert sent status: {budget.alert_sent}")
    
    # Verify messages
    messages = [m.message for m in storage]
    print(f"Messages generated: {messages}")

    if budget.alert_sent and len(messages) > 0:
        print("Verification SUCCESS: Budget connected and alerts triggered!")
    else:
        print("Verification FAILED: Budget connected but alerts not triggered.")

if __name__ == "__main__":
    verify_budget_logic()
