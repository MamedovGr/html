from django.urls import path
from .views import *
from higgs import routers
from . import handlers

router = routers.SimpleRouter('main')

router.register('customers')
router.register('stores')
router.register('employees')

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('reports/', ReportsView.as_view(), name='reports'),
    path('reports-loan/', LoanReportsView.as_view(), name='loan-reports'),
] + router.urls

# handler urlpatterns

handler_urlpatterns = [
    path('customer-lock-toggle/<int:pk>/', handlers.customer_lock_toggle, name='customer-lock-toggle'),
    path('customer-blacklist-toggle/<int:pk>/', handlers.customer_blacklist_toggle, name='customer-blacklist-toggle'),
    path('customer-lock-query/', handlers.customer_lock_query, name='customer-lock-query'),
    path('customer-unlock-query/', handlers.customer_unlock_query, name='customer-unlock-query'),
    path('export-reports-xls', handlers.export_reports_xls, name='export_reports_xls'),
    path('export-loans-xls', handlers.export_loans_xls, name='export_loans_xls'),
    path('switch/store/<int:pk>/', handlers.switch_store, name='switch_store'),
    path('switch/store/all/', handlers.switch_store_to_all, name='switch_store_to_all'),
]

urlpatterns += handler_urlpatterns
