from . import views
from django.urls import path

urlpatterns = [
    # vendor Api
    path('vendors/',views.VendorList,name="vendorlist"),
    path('vendors/<int:id>',views.VendorInfo,name="VendorInfo"),
    path('vendors/delete/<int:id>',views.DeleteVendor,name="deletevendor"),
    path('vendors/edit/<int:id>',views.UpdateVendor,name="updatevendor"),
    # path('vendor/<int:id>',views.VendorUpdate,name="updatevendor"),

    #Puchase Api
    path('purchase/',views.PurchaseOrderList,name="PurchaseOrder"),
    path('purchase/filter/<int:id>',views.PurchaseFilter,name="Purchasefilter"),
    path('purchase/<int:id>',views.PurchaseDetail,name="PurchaseDetail"),
    path('purchase/delete/<int:id>',views.DeletePurchaseOrder,name="deletepurchaseorder"),

    # For Acknowledgement 
    path('purchase/<int:id>/acknowledgment',views.PurchaseAcknowledgement,name="purchaseacnowledgement"),

    # For performance
    path('vendors/<int:id>/performance',views.PerformanceMatric,name="performancematric")
]