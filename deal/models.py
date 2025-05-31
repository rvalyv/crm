from django.db import models
from contacts.models import Contact
from django.conf import settings

class Deal(models.Model):
    STATUS_CHOICES = [
        ('open', 'New'),
        ('won', 'Done'),
        ('lost', 'Lose'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'USD'),
        ('UZS', 'UZS'),
    ]

    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='deals')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    close_date = models.DateTimeField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_deals')

    def __str__(self):
        return f"{self.title} - {self.contact.name}"
