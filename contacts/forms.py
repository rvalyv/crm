from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'status', 'deal_price', 'currency', 'notes']
        exclude = ['deal_price', 'currency']

        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'deal_price': forms.NumberInput(attrs={
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '(90)-123-45-67',
                'id': 'phone-number'
            })
        }

        labels = {
            'deal_price': 'Deal Price (optional)',
            'currency': 'Currency'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only access fields if they exist
        for field_name in ['phone', 'email', 'status']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        cleaned_phone = phone.replace(' ', '')
        return cleaned_phone
