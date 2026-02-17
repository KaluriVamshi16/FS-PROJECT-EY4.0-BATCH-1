from django.urls import path
from .views import dashboard_view
from .api_views import DashboardDataView

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('api/data/', DashboardDataView.as_view(), name='dashboard_data'),
]
