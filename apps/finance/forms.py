from django.forms import inlineformset_factory, modelformset_factory
from django import forms

from .models import Invoice, InvoiceItem, Receipt
class CustomChildForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ["amount_paid", "date_paid", "comment"]
        widgets = {
            'date_paid': forms.DateTimeInput(format='%d-%m-%Y %H:%M:%S'),
        }

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=["description", "amount"], extra=1, can_delete=True
)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice,
    Receipt,
    form=CustomChildForm,
    extra=1,
    can_delete=True,
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)
