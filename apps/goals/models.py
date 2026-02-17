from django.db import models
from django.contrib.auth.models import User
from datetime import date

class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    icon = models.CharField(max_length=10, default='🎯')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def monthly_saving_required(self):
        today = date.today()
        months_left = max(1, (self.target_date.year - today.year) * 12 +
                         (self.target_date.month - today.month))
        return (self.target_amount - self.current_amount) / months_left

    @property
    def progress_percentage(self):
        if not self.target_amount:
            return 0
        return int(min(100, (self.current_amount / self.target_amount) * 100))
