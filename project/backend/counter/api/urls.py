from django.urls import path
from .views import (
    CounterListCreateView, CounterTickCreateView, DailyCounterListView
)

app_name = 'counter'

urlpatterns = [
    path('', CounterListCreateView.as_view(), name='counter-list-create'),
    path('all/', DailyCounterListView.as_view(), name='counter-all-list'),
    path('tick/', CounterTickCreateView.as_view(), name='counter-tick-create'),
    # path('<int:id>', )
]
