from django import forms
from .models import PurchaseOrder

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'items', 'quantity', 'quality_rating']
        labels = {
            'vendor': 'Choose Vendor',
            'items': 'Enter Your Items detail',
            'quentity': 'Enter Quentity',
            'quality_rating': 'Quality Rating ( 0 to 10 )',
        }