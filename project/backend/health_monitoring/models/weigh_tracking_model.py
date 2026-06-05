from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError

User = get_user_model()


class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weight_entries")
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    date = models.DateField()

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
        constraints = [
            models.CheckConstraint(
                condition=Q(weight__gt=0),
                name="weight_positive",
            )
        ]


    def clean(self):
        if self.date and self.date > timezone.now().date():
            raise ValidationError("Gelecek bir tarihe ait kilo bilgisi eklenemez.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.weight} kg on {self.date}"
