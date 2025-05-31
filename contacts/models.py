from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('failed', 'Failed'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True)
    deal_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Deal Price (optional)"
    )
    currency = models.CharField(
        max_length=3,
        default='USD',
        choices=[('USD', 'USD'), ('USZ', 'USZ')],
        blank=True
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_leads'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_leads',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = self.assigned_to
        super().save(*args, **kwargs)

    def formatted_phone(self):
        if self.phone:
            return f"+998({self.phone[:2]})-{self.phone[2:5]}-{self.phone[5:7]}-{self.phone[7:9]}"
        return self.phone