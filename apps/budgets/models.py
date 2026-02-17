from django.db import models
from django.contrib.auth.models import User
from apps.expenses.models import ExpenseCategory

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField() # First of month
    alert_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} Budget - {self.month}"

    @property
    def spent(self):
        from apps.expenses.models import Expense
        from django.db.models import Sum
        # Filter expenses for this user, category, and month
        total = Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__year=self.month.year,
            date__month=self.month.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return float(total)
    
    @property
    def percentage_used(self):
        if self.monthly_limit == 0:
            return 0
        return (self.spent / float(self.monthly_limit)) * 100
