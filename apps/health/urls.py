from django.urls import path
from .views import health_score_view

urlpatterns = [
    path('', health_score_view, name='health_score_view'),
]
