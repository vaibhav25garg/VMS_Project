from django.db import models
from django.db.models import JSONField
from django.utils import timezone
from django.utils.dateparse import parse_datetime

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Vendor Name')
    email = models.EmailField(verbose_name='Email',null=True)
    phone_number = models.CharField(max_length=20, verbose_name='Phone Number',null=True)
    delivery_days = models.IntegerField(verbose_name='Total Day Deliver', null=True)
    address = models.TextField(verbose_name='Address', null=True)
    vendor_code = models.CharField(max_length=20, unique=True, verbose_name='Vendor Code', blank=True)
    on_time_delivery_rate = models.FloatField(verbose_name='On-Time Delivery Rate',blank=True, null=True)
    quality_rating_avg = models.FloatField(verbose_name='Quality Rating Average',blank=True, null=True)
    average_response_time = models.FloatField(verbose_name='Average Response Time',blank=True, null=True)
    fulfillment_rate = models.FloatField(verbose_name='Fulfillment Rate',blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.vendor_code:  # If vendor code is not provided, generate it
            # Generating the vendor code
            last_vendor = Vendor.objects.last()  # Get the last vendor object
            
            if last_vendor:  # If there are existing vendor objects
                last_code = last_vendor.vendor_code.split('-')[1]  # Extract the last five digits of the last vendor code
                new_code = int(last_code) + 1  # Increment the last five digits by 1
            else:  # If there are no existing vendor objects
                new_code = 1  # Start with 1
            
            self.vendor_code = f"V-{new_code:05d}"  # Format the new code with leading zeros to ensure it's five digits
            
        super().save(*args, **kwargs)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True, verbose_name='PO Number', blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Vendor')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Order Date', blank=True)
    delivery_date = models.DateTimeField(blank=True, null=True, verbose_name='Delivery Date')
    items = JSONField(verbose_name='Items')
    quantity = models.IntegerField(verbose_name='Quantity')
    status = models.CharField(max_length=100, verbose_name='Status',blank=True, default='Pending')
    quality_rating = models.FloatField(null=True, verbose_name='Quality Rating',blank=True)
    issue_date = models.DateTimeField(verbose_name='Issue Date',blank=True, null=True)
    acknowledgment_date = models.DateTimeField(null=True, verbose_name='Acknowledgment Date')

    _delivery_date_set = models.BooleanField(default=False, editable=False)  # Flag to track if delivery_date is set

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if not self.pk:  # Only set order_date if it's a new instance
            self.order_date = timezone.now()
        
        if self.vendor and self.order_date:
            total_delivery_days = self.vendor.delivery_days
            self.delivery_date = self.order_date + timezone.timedelta(days=total_delivery_days)
            self._delivery_date_set = True  # Set the flag to True after setting the delivery_date

        if not self.po_number:  # If vendor code is not provided, generate it
            # Generating the vendor code
            last_vendor = PurchaseOrder.objects.last()  # Get the last vendor object
            
            if last_vendor:  # If there are existing vendor objects
                last_code = last_vendor.po_number.split('-')[1]  # Extract the last five digits of the last vendor code
                new_code = int(last_code) + 1  # Increment the last five digits by 1
            else:  # If there are no existing vendor objects
                new_code = 1  # Start with 1
            
            self.po_number = f"PO-{new_code:05d}"  # Format the new code with leading zeros to ensure it's five digits

        super().save(*args, **kwargs)

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    class Meta:
        verbose_name = "Historical Performance"
        verbose_name_plural = "Historical Performances"

    def save(self, *args, **kwargs):
        # Ensure all required fields are set before saving
        if self.date is None:
            self.date = timezone.now()
        # You might want to add similar checks for other fields here

        super().save(*args, **kwargs)  # Call the save method of the parent class'

    def __str__(self):
        return f"{self.vendor} - {self.date}"