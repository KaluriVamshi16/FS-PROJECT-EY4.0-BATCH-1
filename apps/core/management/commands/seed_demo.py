from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.expenses.models import Expense, ExpenseCategory
from apps.budgets.models import Budget
from apps.goals.models import FinancialGoal
from apps.dashboard.models import Income
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seeds database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        
        # Create Demo User
        user, created = User.objects.get_or_create(username='demo')
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write('Created user: demo / demo123')
        
        # Categories
        categories = ['Food', 'Travel', 'Rent', 'Shopping', 'Entertainment', 'Utilities', 'Healthcare']
        cat_objs = {}
        for cat in categories:
            obj, _ = ExpenseCategory.objects.get_or_create(name=cat, user=user)
            cat_objs[cat] = obj

        # Income
        Income.objects.get_or_create(user=user, source="Salary", amount=50000, month=timezone.now().date().replace(day=1))
        
        # Budgets
        Budget.objects.get_or_create(user=user, category=cat_objs['Food'], monthly_limit=10000, month=timezone.now().date().replace(day=1))
        Budget.objects.get_or_create(user=user, category=cat_objs['Travel'], monthly_limit=5000, month=timezone.now().date().replace(day=1))

        # Goals
        FinancialGoal.objects.get_or_create(user=user, title="Emergency Fund", target_amount=100000, current_amount=20000, target_date=timezone.now().date() + timedelta(days=365))

        # Expenses (Random 30)
        for _ in range(30):
            cat = random.choice(categories)
            amount = random.randint(100, 2000)
            date = timezone.now() - timedelta(days=random.randint(0, 60))
            Expense.objects.create(
                user=user,
                category=cat_objs[cat],
                amount=amount,
                description=f"Demo expense for {cat}",
                date=date,
                created_via_chat=False
            )
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded demo data.'))
