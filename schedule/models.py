from django.db import models


class Meeting(models.Model):
    """Model representing a scheduled meeting in the Sky Health Check system."""

    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    PLATFORM_CHOICES = [
        ('Microsoft Teams', 'Microsoft Teams'),
        ('Zoom', 'Zoom'),
        ('In Person', 'In Person'),
        ('Google Meet', 'Google Meet'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, default='Microsoft Teams')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Scheduled')
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} – {self.team} ({self.date})"