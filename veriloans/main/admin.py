from django.contrib import admin
from .models import (
    Store,
    Customer,
)

admin.site.register(Store)
admin.site.register(Customer)
