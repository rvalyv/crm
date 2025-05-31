from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'assigned_to', 'deal_price', 'currency')
    list_filter = ('status', 'assigned_to')
    search_fields = ('name', 'email')