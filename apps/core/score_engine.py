def calculate_health_score(user, monthly_income, monthly_expenses, savings, total_budgets, budgets_exceeded, goal_progress_avg):
    """
    Calculates Financial Health Score (0-100)
    """
    score = 0
    tips = []
    
    # 1. Savings Rate Score (0-30 points)
    if monthly_income > 0:
        savings_rate = (savings / monthly_income) * 100
    else:
        savings_rate = 0
        
    if savings_rate >= 20:
        score += 30
    elif 10 <= savings_rate < 20:
        score += 20
        tips.append("Try to increase your savings rate to 20%.")
    elif 0 < savings_rate < 10:
        score += 10
        tips.append("Aim to save at least 10% of your income.")
    else:
        tips.append("Your expenses exceed or match your income. Start saving small amounts.")

    # 2. Expense Ratio Score (0-30 points)
    if monthly_income > 0:
        expense_ratio = (monthly_expenses / monthly_income) * 100
    else:
        expense_ratio = 100 # Assume worst case if no income
        
    if expense_ratio < 50:
        score += 30
    elif 50 <= expense_ratio < 70:
        score += 20
    elif 70 <= expense_ratio < 90:
        score += 10
        tips.append("Your expenses are high (>70% of income). Review your spending.")
    else:
        tips.append("Critical: You are spending almost everything you earn.")

    # 3. Budget Discipline Score (0-20 points)
    if total_budgets > 0:
        budget_score = ((total_budgets - budgets_exceeded) / total_budgets) * 20
        score += budget_score
        if budgets_exceeded > 0:
            tips.append(f"You exceeded {budgets_exceeded} budgets. Try to stick to your limits.")
    else:
        score += 10 # Neutral if no budgets
        tips.append("Set budgets to track your spending limits.")

    # 4. Goal Progress Score (0-20 points)
    score += (goal_progress_avg * 0.20)
    if goal_progress_avg < 50:
        tips.append("You are behind on your financial goals.")

    final_score = int(min(100, max(0, score)))
    
    grade = 'F'
    if final_score >= 90: grade = 'A+'
    elif final_score >= 80: grade = 'A'
    elif final_score >= 70: grade = 'B'
    elif final_score >= 60: grade = 'C'
    elif final_score >= 40: grade = 'D'
    
    return {
        "total": final_score,
        "grade": grade,
        "tips": tips[:3] # Return top 3 tips
    }
