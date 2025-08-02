from rest_framework.generics import RetrieveUpdateDestroyAPIView
from counter.models import Counter


class CounterRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Counter.objects.filter(user=self.request.user)

