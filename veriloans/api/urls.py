from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('custobbbmers/', views.customers),
    path('stores/<int:id>/', views.store),
    path('employees/<int:id>/', views.employee),
    path('loans/<int:id>/', views.loan),
    path('loans/by_passport/', views.get_loans_by_passport), # API for Mobile
    path('loans-with-details/', views.get_loans_with_details), # API for Mobile
]
