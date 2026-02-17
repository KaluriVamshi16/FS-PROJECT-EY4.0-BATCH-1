from django.contrib import admin
from .models import Expense, ExpenseCategory

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'date', 'source')
    list_filter = ('category', 'date', 'source')
    search_fields = ('description',)

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
