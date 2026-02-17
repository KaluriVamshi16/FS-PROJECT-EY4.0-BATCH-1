from django.contrib import admin
from .models import FinancialHealthScore

@admin.register(FinancialHealthScore)
class FinancialHealthScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'calculated_at')
