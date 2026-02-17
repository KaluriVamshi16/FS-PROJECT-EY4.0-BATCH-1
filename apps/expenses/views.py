from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
import json

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Python Aggregation to avoid SQLite TruncDate issues
    category_totals = {}
    daily_totals = {}

    for expense in expenses:
        # Pie Chart: Category
        cat_name = expense.category.name if expense.category else 'Uncategorized'
        category_totals[cat_name] = category_totals.get(cat_name, 0) + float(expense.amount)

        # Line Chart: Daily
        date_str = expense.date.strftime('%Y-%m-%d')
        daily_totals[date_str] = daily_totals.get(date_str, 0) + float(expense.amount)

    # Sort Category Data (Highest first)
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    pie_labels = [k for k, v in sorted_cats]
    pie_data = [v for k, v in sorted_cats]

    # Sort Daily Data (Chronological)
    sorted_days = sorted(daily_totals.items())
    line_labels = [k for k, v in sorted_days]
    line_data = [v for k, v in sorted_days]

    context = {
        'expenses': expenses,
        'pie_labels': json.dumps(pie_labels),
        'pie_data': json.dumps(pie_data),
        'line_labels': json.dumps(line_labels),
        'line_data': json.dumps(line_data),
    }
    return render(request, 'expenses/index.html', context)

@login_required
def add_expense(request):
    print(f"DEBUG: User accessing add_expense: {request.user}")
    from .models import ExpenseCategory
    count = ExpenseCategory.objects.filter(user=request.user).count()
    print(f"DEBUG: Category count for user: {count}")
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            # Check for budget alerts after adding expense
            try:
                from apps.budgets.utils import check_and_alert_budgets
                check_and_alert_budgets(request)
            except Exception as e:
                print(f"Error checking budget alerts: {e}")
                
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)
    
    return render(request, 'expenses/add_expense.html', {'form': form})
