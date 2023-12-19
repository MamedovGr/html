from django.urls import path
from . import views

app_name = 'scripts'

urlpatterns = [
    path('import-customers-csv/', views.import_customers_csv),
    path('import-loans-csv/', views.import_loans_csv),
    path('import-transactions-csv/', views.import_transactions_csv),
]
