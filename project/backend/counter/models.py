from django.db import models
from django.contrib.auth.models import User

class Counter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # örn: Tuvalet, Sigara, Su İçme
    unit = models.CharField(max_length=50, blank=True, null=True)  # isteğe bağlı: 'kez', 'adet'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class CounterEntry(models.Model):
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name="entries")
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.IntegerField(default=1)  # Genelde 1, ama kullanıcı isterse farklı değer de ekleyebilir

    def __str__(self):
        return f"{self.counter.name} - {self.timestamp.date()} - {self.value}"
