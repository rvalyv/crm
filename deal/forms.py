from django import forms
from .models import Deal

class DealForm(forms.ModelForm):
    close_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%d-%m-%YT%H:%M']
    )

    class Meta:
        model = Deal
        fields = ['title', 'amount', 'currency', 'contact', 'status', 'close_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
