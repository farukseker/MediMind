from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DailyNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    note = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class NoteType(models.TextChoices):
        ASK_TO_DOCTOR = "ask_to_doctor", "Ask to Doctor"
        NOTE = "note", "Note"
        ONLY_ME_NOTE = "only_me_note", "Only Me Note"

    note_type = models.CharField(
        max_length=20,
        choices=NoteType.choices,
        default=NoteType.NOTE
    )

    class Meta:
        verbose_name = "Daily Note"
        verbose_name_plural = "Daily Notes"
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"Note for {self.user.username} on {self.date}"
