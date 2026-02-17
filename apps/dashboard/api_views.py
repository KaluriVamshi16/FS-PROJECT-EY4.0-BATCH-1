from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Sum
from datetime import datetime, timedelta

class DashboardDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.expenses.models import Expense
        user = request.user
        today = datetime.now()
        first_day_of_month = today.replace(day=1)
        
        # Monthly Spending
        monthly_expenses = Expense.objects.filter(
            user=user, 
            date__gte=first_day_of_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Category-wise
        category_expenses = Expense.objects.filter(
            user=user,
            date__gte=first_day_of_month
        ).values('category__name').annotate(total=Sum('amount'))
        
        data = {
            "monthly_spending": monthly_expenses,
            "category_data": list(category_expenses)
        }
        return Response(data)
