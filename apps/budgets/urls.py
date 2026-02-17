from django.urls import path
from .views import budget_list, add_budget

urlpatterns = [
    path('', budget_list, name='budget_list'),
    path('add/', add_budget, name='add_budget'),
]
