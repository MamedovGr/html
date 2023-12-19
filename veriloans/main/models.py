from django.db import models
from accounts.models import Employee
from .managers import ProductQuerySet, CustomerQuerySet, StoreQuerySet
from django.urls import reverse
from datetime import datetime

from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your models here.
class Characteristic(models.Model):
    visible = models.BooleanField(default=True)
    editable = models.BooleanField(default=True)
    deletable = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Store(Characteristic):
    title = models.CharField(max_length=255)
    address = models.TextField()
    code = models.CharField(max_length=255, blank=True, null=True)
    last_loan_id = models.PositiveIntegerField(default=0)
    employees = models.ManyToManyField(Employee)
    objects = StoreQuerySet.as_manager()

    class Meta:
        ordering = ('-id',)

    def workers(self):
        return [employee for employee in self.employees.all() if employee.status.title != 'super-admin']

    def serializer(self):
        return {
            'id': self.id,
            'title': self.title,
            'address': self.address,
            'code': self.code,
            'employees': [x.id for x in self.employees.exclude(status__title='super-admin')],
        }

    def __str__(self):
        return self.title


class Customer(Characteristic):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True)
    passport_id = models.CharField(max_length=255, unique=True)
    passport_created_date = models.DateTimeField(blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    county = models.CharField(max_length=255)
    registration = models.TextField()
    work_place = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255)
    limit = models.IntegerField(default=0, blank=True)
    phone = models.CharField(max_length=64)
    phone2 = models.CharField(max_length=64)
    phone3 = models.CharField(max_length=64)
    notes = models.TextField(blank=True)
    file = models.FileField(upload_to="customers/file/", null=True)
    file2 = models.FileField(upload_to="customers/file2/", null=True)
    in_blacklist = models.BooleanField(default=False)
    objects = CustomerQuerySet.as_manager()

    class Meta:
        ordering = ('-id',)

    def get_loans(self):
        customer_loans_for_mobile = [ loan.mobile_serializer() for loan in self.loan_set.filter(is_closed=False, is_draft=False) ]
        return customer_loans_for_mobile

    def save(self):
        # Opening the uploaded image

        if self.file:
            im = Image.open(self.file)
            image_format = im.format.lower()
            output = BytesIO()
            # Resize/modify the file
            a, b = im.size
            im = im.resize((int(a/2), int(b/2)), Image.ANTIALIAS)

            # after modifications, save it to the output
            im.save(output, format=image_format, quality=95, optimize=True)
            output.seek(0)
            # change the filefield value to be the newley modifed file value
            self.file = InMemoryUploadedFile(output, 'ImageField', f"{self.file.name.split('.')[0]}.{image_format}", f'image/{image_format}', sys.getsizeof(output), None)

        if self.file2:
            im = Image.open(self.file2)
            image_format = im.format.lower()
            output = BytesIO()
            # Resize/modify the file2
            a, b = im.size
            im = im.resize((int(a/2), int(b/2)), Image.ANTIALIAS)

            # after modifications, save it to the output
            im.save(output, format=image_format, quality=95, optimize=True)
            output.seek(0)
            # change the file2field value to be the newley modifed file2 value
            self.file2 = InMemoryUploadedFile(output, 'ImageField', f"{self.file2.name.split('.')[0]}.{image_format}", f'image/{image_format}', sys.getsizeof(output), None)

        super().save()

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    def get_absolute_url(self):
        return reverse('customers-detail', args=[str(self.id)])

    def get_file(self):
        if self.file:
            return self.file.url

    def get_file2(self):
        if self.file2:
            return self.file2.url

    def get_payment_amount(self):
        return sum([ loan.amount_price for loan in self.loan_set.filter(is_draft=False, is_closed=False) ])

    def serializer(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'patronymic': self.patronymic,
            'full_data': f'{self.__str__()} ( {self.phone} ) [{self.passport_id}]',
            'passport_id': self.passport_id,
            'phone': self.phone,
            'in_blacklist': self.in_blacklist,
        }

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
