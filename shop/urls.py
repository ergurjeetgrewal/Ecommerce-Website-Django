from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name="ShopHome"),
    path('about/', views.about,name="AboutUs"),
    path('contact/', views.contact,name="ContactUs"),
    path('tracker/', views.tracker,name="TrackingStatus"),
    path('search/', views.search,name="Search"),
    path('products/<int:proid>', views.productView,name="ProductView"),
    path('checkout/', views.checkout,name="Checkout"),
    path('termsandconditions/', views.termsandconditions,name="TermsConditions"),
    path('privacy/', views.privacy,name="Privacy"),
    path('paymenthandler/', views.paymenthandler,name="paymenthandler"),
    # path('paymentstatus/', views.paymentstatus,name="paymentstatus"),
]
