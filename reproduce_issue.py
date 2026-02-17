import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finsight.settings')
django.setup()

from apps.expenses.models import Expense
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncDate

user = User.objects.first()
print(f"Testing for user: {user}")

print("Testing usage of Sum...")
try:
    category_data = Expense.objects.filter(user=user).values('category__name').annotate(total=Sum('amount')).order_by('-total')
    print(list(category_data))
    print("Sum success")
except Exception as e:
    print(f"Sum failed: {e}")

print("Testing usage of TruncDate...")
try:
    daily_data = Expense.objects.filter(user=user).annotate(date_only=TruncDate('date')).values('date_only').annotate(total=Sum('amount')).order_by('date_only')
    print(list(daily_data))
    print("TruncDate success")
except Exception as e:
    print(f"TruncDate failed: {e}")
