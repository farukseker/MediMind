from django.db.models.functions import Coalesce
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from counter.api.serializers import CounterStatusCreateSerializer
from counter.models import Counter
from django.db.models import Sum, Value, Q
from datetime import date


class CounterListCreateView(ListCreateAPIView):
    serializer_class = CounterStatusCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # today = date.today()
        # return (
        #     Counter.objects.filter(user=self.request.user)
        #     .annotate(
        #         # count=Coalesce(Sum('entries__value'), Value(0)),
        #         count=Coalesce(Sum('entries__value', filter=Q(entries__timestamp__date=today)), Value(0))
        #     )
        # )
        return Counter.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, **serializer.validated_data)
