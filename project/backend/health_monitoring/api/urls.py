from django.urls import path
from django.urls.resolvers import RoutePattern

from health_monitoring.api.views import *

app_name = "health_monitoring_api"

water_urlpatterns: list[path:RoutePattern] = [
    path('water/entries/<int:pk>/', WaterEntryDeleteView.as_view(), name='water-entry-delete'),
    path('water/entries/<str:date>/', WaterEntryListCreateView.as_view(), name='water-entries-by-date'),
    path('water/entries/', WaterEntryListCreateView.as_view(), name='water-entries-all'),
    path('water/goal/', WaterGoalView.as_view(), name='water-goal')
]

weight_urlpatterns: list[path:RoutePattern] = [
    path('weight/entries/', WeightEntryListCreateView.as_view(), name='weight-entry'),
    path('weight/entries/<int:pk>/', WeightEntryDeleteView.as_view(), name='weight-entry-delete'),
]

urlpatterns = water_urlpatterns + weight_urlpatterns