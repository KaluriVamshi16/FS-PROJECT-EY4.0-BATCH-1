from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FinancialGoal
from .forms import FinancialGoalForm

@login_required
def goal_list(request):
    goals = FinancialGoal.objects.filter(user=request.user).order_by('target_date')
    
    if request.method == 'POST':
        form = FinancialGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            if not goal.icon:
                goal.icon = '🎯'
            goal.save()
            return redirect('goal_list')
    else:
        form = FinancialGoalForm()

    return render(request, 'goals/index.html', {'goals': goals, 'form': form})
