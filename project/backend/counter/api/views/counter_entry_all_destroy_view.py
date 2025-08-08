from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from counter.models import Counter


class CounterEntryAllDestroyView(APIView):

    @staticmethod
    def delete(request, counter_pk):
        counter = get_object_or_404(
            Counter,
            user=request.user,
            pk=counter_pk
        )
        deleted_count, _ = counter.entries.all().delete()
        return Response(
            {"message": f"{deleted_count} entries deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
