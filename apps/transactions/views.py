from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.expenses.models import Expense
from apps.dashboard.models import Income, Investment
from itertools import chain
from operator import attrgetter

from .forms import AddTransactionForm
from django.shortcuts import redirect

@login_required
def transaction_list(request):
    expenses = Expense.objects.filter(user=request.user)
    incomes = Income.objects.filter(user=request.user)
    investments = Investment.objects.filter(user=request.user)

    # Normalize data for the template
    for e in expenses:
        e.type = 'debit'
        e.title = e.description or f"Expense: {e.category.name}"
        e.cat_name = e.category.name
        
    for i in incomes:
        i.type = 'credit'
        i.title = i.source
        i.cat_name = 'Income'
        i.date = i.month # Map month to date for sorting
        
    for inv in investments:
        inv.type = 'debit'
        inv.title = f"Investment: {inv.name}"
        inv.cat_name = 'Investment'

    # Combine and sort
    transactions = sorted(
        chain(expenses, incomes, investments),
        key=attrgetter('date'),
        reverse=True
    )

    return render(request, 'transactions/index.html', {'transactions': transactions})

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = AddTransactionForm(request.user, request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            if type == 'expense':
                category = form.cleaned_data['expense_category']
                Expense.objects.create(
                    user=request.user,
                    amount=amount,
                    category=category,
                    date=date,
                    description=description,
                    source='manual'
                )
            elif type == 'income':
                source = form.cleaned_data['income_source']
                # Use description if source matches label, or combine
                final_source = source if source else description
                Income.objects.create(
                    user=request.user,
                    amount=amount,
                    source=final_source,
                    month=date # saving date to month field
                )
            
            return redirect('transaction_list')
    else:
        form = AddTransactionForm(request.user)
    
    return render(request, 'transactions/add_transaction.html', {'form': form})
