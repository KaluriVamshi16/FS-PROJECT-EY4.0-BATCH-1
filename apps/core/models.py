from django.db import models
from django.contrib.auth.models import User

class FinancialHealthScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_scores')
    score = models.IntegerField() # 0-100
    calculated_at = models.DateTimeField(auto_now_add=True)
    breakdown = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
