from django.contrib import admin
from django.urls import path, include
from apps.core.views import landing_page
from apps.core.settings_views import settings_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('', landing_page, name='landing'),
    path('settings/', settings_view, name='settings'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('budgets/', include('apps.budgets.urls')),
    path('goals/', include('apps.goals.urls')),
    path('insights/', include('apps.insights.urls')),
    path('transactions/', include('apps.transactions.urls')),
    path('health/', include('apps.health.urls')),
    path('financials/', include('apps.financials.urls')),
    path('api/chat/', include('apps.chatbot.urls')),
]
