from django.urls import path
from .views import *


app_name = 'counter'

urlpatterns = [
    path('', CounterListCreateView.as_view(), name='counter-list-create'),
    path('all/', DailyCounterListView.as_view(), name='counter-all-list'),
    path('tick/', CounterTickCreateView.as_view(), name='counter-tick-create'),
    path('<int:pk>/', CounterRetrieveUpdateDestroyView.as_view(), name='counter-crud'),

    path('<int:counter_pk>/entry/', CounterEntryGroupedRetrieveDestroyListView.as_view(), name="counter-grouped-entry-crud"),
    # path('<int:counter_pk>/entry/delete-all/', CounterEntryGroupedRetrieveDestroyListView.as_view(), name="counter-remove-all-entries"),
    path('<int:counter_pk>/entry/<int:delete_index>/', CounterEntryGroupedRetrieveDestroyListView.as_view(), name="counter-remove-entry-range-from-index"),

]
