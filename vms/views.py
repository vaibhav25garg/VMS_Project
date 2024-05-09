from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.http import HttpRequest  # Add this line to import the HttpRequest module
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from django.views import View
from .forms import PurchaseOrderForm
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.db.models import Count, Avg
from django.contrib import messages



# Vendor Operations

def home(request):
    return render(request, 'Home.html')

# Show all Vendor in List 
def VendorList(request):
    ven = Vendor.objects.all()

    if request.method == 'POST':
        name = request.POST.get('vendorName')
        email = request.POST.get('Email')
        phone = request.POST.get('contactNo')
        address = request.POST.get('address')
        delivertime = request.POST.get('DeliveryDays')

        addvendor = Vendor(
            name=name,
            email=email,
            phone_number=phone,
            address=address,
            delivery_days=delivertime
        )
        addvendor.save()
        messages.success(request, 'New Vendor Added successfully!')
        return redirect('vendorlist')

    context = {
        'ven': ven,
    }
    return render(request, "vendor_list.html", context)

# Show Vendor dertails on specific id 
def VendorInfo(request, id):
    # ven = Vendor.objects.get(id=id)
    ven = get_object_or_404(Vendor, pk=id)
    pur = PurchaseOrder.objects.filter(vendor_id = id)

    if request.method == 'POST':
        ven.name = request.POST.get('vendorName')
        ven.email = request.POST.get('email')
        ven.phone = request.POST.get('contactDetails')
        ven.address = request.POST.get('address')
        ven.delivertime = request.POST.get('diliveryDays')
        ven.save()  # Save the updated vendor object
        messages.success(request, 'Vendor Information Updated successfully!')
        return redirect('VendorInfo', id=id) 

    context = {
        'ven':ven,
        'pur':pur
    }
    return render(request,"vendor_info.html",context)

# Delete single Vendor 
def DeleteVendor(request, id):
    if id == 0:
        Vendor.objects.all().delete()
        messages.success(request, 'All Vendors Deleted successfully!')
    else:
        ven = Vendor.objects.get(id=id)
        messages.success(request, 'Vendor Delete')
        ven.delete()
    return redirect("vendorlist")

# Update single Vendor 
def UpdateVendor(request, id):
    ven = get_object_or_404(Vendor, pk=id)

    if request.method == 'POST':
        ven.name = request.POST.get('vendorName')
        ven.email = request.POST.get('email')
        ven.phone = request.POST.get('contactDetails')
        ven.address = request.POST.get('address')
        ven.delivertime = request.POST.get('diliveryDays')
        ven.save()  # Save the updated vendor object
        messages.success(request, 'Vendor Information Updated successfully!')
        return redirect('updatevendor', id=id) 

    context = {
        'ven': ven,
    }
    return render(request, "vendor_list.html", context)

# Purchase Operation

# Show all purchase Order in list 
def PurchaseOrderList(request):
    pur = PurchaseOrder.objects.all()
    ven = Vendor.objects.all()
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Order Generate successfully!')
            return redirect('PurchaseOrder')  # Redirect to a list view after successful form submission
    else:
        form = PurchaseOrderForm()
        
    context = {
        'pur':pur,
        'form': form,
        'ven':ven,
    }
    return render(request,"purchase_order.html",context)

# show Purchase order by filter vendor id
def PurchaseFilter(request, id):
    # Retrieve the vendor's purchase data
    pur = PurchaseOrder.objects.filter(vendor_id=id)
    ven = Vendor.objects.all()
    context = {
        'pur':pur,
        'ven':ven
    }
    return render(request,"purchase_order.html",context)

# show purchase order detaail on specific puchase-order id
def PurchaseDetail(request, id):
    pur = PurchaseOrder.objects.get(id=id)

    # this condition will update purchase detail
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST, instance=pur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Updated successfully!')
            return redirect('PurchaseDetail', id=id)  # Redirect to a list view after successful form submission
    else:
        form = PurchaseOrderForm(instance=pur)
    
    # update_performance_metrics(id) 
    context = {
        'pur':pur,
        'form': form,
    }
 
    return render(request,"purchase_detail.html", context)

# Delete single purchase order detail on base of id
def DeletePurchaseOrder(request, id):
    if id == 0:
        PurchaseOrder.objects.all().delete()
        messages.success(request, 'All Order Deleted successfully!')
    else:
        ven = PurchaseOrder.objects.get(id=id)
        ven.delete()
        messages.success(request, 'Order Deleted successfully!')
    return redirect("PurchaseOrder")

# Acknoeledgement and trigger for recalculation
def PurchaseAcknowledgement(request, id):
    pur = get_object_or_404(PurchaseOrder, id=id)

    if request.method == 'POST':
        acknowledge = request.POST.get('Acknowledge')
        issue = request.POST.get('issue')
        status = request.POST.get('status')
    
        if acknowledge == "Confirm" or acknowledge == "Not Available":
            pur.acknowledgment_date = timezone.now()

        if status == "completed":
            pur.issue_date = timezone.now()

        pur.status = status  # Update status

        pur.save()  # Save the updated PurchaseOrder object
        return redirect('purchaseacnowledgement', id=id)
    # update_performance_metrics(id)
    context = {
        'pur': pur
    }
    
    return render(request, "purchase_detail_edit.html", context)

# Perfromance calculations

def update_performance_metrics(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    ven = Vendor.objects.get(name=vendor)

    total_completed_pos = completed_pos.count()

    # # On-Time Delivery Rate
    on_time_delivery_pos = completed_pos.filter(delivery_date__gte=F('issue_date'))
    on_time_delivery_count = on_time_delivery_pos.count()
    on_time_delivery_rate = on_time_delivery_count / total_completed_pos if total_completed_pos != 0 else 0
    on_time_delivery_rate = on_time_delivery_rate * 10
    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, defaults={'on_time_delivery_rate': on_time_delivery_rate})
    ven.on_time_delivery_rate = on_time_delivery_rate

    # # Quality Rating Average
    quality_rating_avg = completed_pos.exclude(quality_rating__isnull=True).aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or 0
    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, defaults={'quality_rating_avg': quality_rating_avg})
    ven.quality_rating_avg = quality_rating_avg

    # Average Response Time
    response_times = completed_pos.exclude(issue_date__isnull=True, acknowledgment_date__isnull=True).annotate(response_time=F('acknowledgment_date') - F('issue_date')).aggregate(avg_response_time=Avg('response_time'))['avg_response_time']
    average_response_time = response_times
    total_seconds = average_response_time.total_seconds()

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    average_response_time = (hours*60)+minutes
    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, defaults={'average_response_time': average_response_time})
    ven.average_response_time = average_response_time

    # Fulfilment Rate
    successful_pos = completed_pos.filter(issue_date__isnull=False, acknowledgment_date__isnull=False, status='completed')
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilment_rate = successful_pos.count() / total_pos if total_pos != 0 else 0
    fulfilment_rate = fulfilment_rate * 100
    historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, defaults={'fulfillment_rate': fulfilment_rate})
    ven.fulfillment_rate = fulfilment_rate
    
    ven.save()

    if not created:
        historical_performance.average_response_time = on_time_delivery_rate
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.average_response_time = average_response_time
        historical_performance.fulfillment_rate = fulfilment_rate
        historical_performance.save()

@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics_on_purchase_order_save(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        update_performance_metrics(instance.vendor)


# Performance Matrics

def PerformanceMatric(request, id):
    perform = HistoricalPerformance.objects.get(vendor_id = id)
    ven = Vendor.objects.get(id=id)
    context={
        'perform':perform,
        'ven':ven
    }
    return render(request, "vendor_performance.html" ,context)