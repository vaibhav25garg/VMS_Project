from django.contrib import admin
from .models import Vendor,PurchaseOrder, HistoricalPerformance

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'email', 'phone_number', 'address', 'vendor_code')
    search_fields = ('name', 'email', 'vendor_code')
    list_filter = ('on_time_delivery_rate', 'quality_rating_avg', 'fulfillment_rate')

admin.site.register(Vendor, VendorAdmin)

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('id','po_number', 'vendor', 'order_date', 'delivery_date', 'status')
    search_fields = ('po_number', 'vendor__name', 'status')
    list_filter = ('status', 'order_date', 'delivery_date')
    date_hierarchy = 'order_date'

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    list_filter = ('vendor', 'date')
    search_fields = ['vendor__name']  # Assuming 'name' is a field in your Vendor model

admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)