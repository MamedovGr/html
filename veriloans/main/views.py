from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from higgs.helpers import without_keys, convert_date
from higgs.db import try_save
from django.http import JsonResponse
from higgs.views import ViewPattern, RequestPost, TemplatePattern
from django.contrib.auth.models import User
from .models import Store, Customer
from accounts.models import Employee, Status
from .contexts import *
from loans.contexts import *
from loans.models import Transaction
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from .handlers import export_reports_xls

class IndexView(LoginRequiredMixin, TemplatePattern, IndexContext):

    def get(self, request, *args, **kwargs):
        if request.session.get('store', '') == '':
            return redirect('accounts:login')
        context = self.get_context_data(request, *args, **kwargs)
        return render(request, 'main/index.html', context)

class CustomerView(LoginRequiredMixin, TemplatePattern, CustomerContext):
    template_name = 'main/customers/index.html'

class CustomerCreateView(LoginRequiredMixin, TemplatePattern):
    template_name = 'main/customers/create.html'

    def post(self, request, *args, **kwargs):

        data = without_keys(request.POST, ['file', 'file2', 'birthday', 'passport_created_date', 'age'])
        object = RequestPost(Customer(), data)
        customer = object.set(commit=False)

        customer.file = request.FILES.get('file', '')
        customer.file2 = request.FILES.get('file2', '')

        if request.POST['age']:
            customer.age = request.POST['age']

        if request.POST['birthday']:
            customer.birthday = convert_date(request.POST['birthday'])

        customer.passport_created_date = convert_date(request.POST['passport_created_date'])

        return redirect('customers') if try_save(request, customer) else redirect('customers-create')

class CustomerDetailView(LoginRequiredMixin, TemplatePattern):
    template_name = 'main/customers/detail.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        context['customer'] = Customer.objects.get(id=kwargs['pk'])

        return context

class CustomerUpdateView(LoginRequiredMixin, TemplatePattern):
    template_name = 'main/customers/update.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        context['customer'] = Customer.objects.get(id=kwargs['pk'])

        return context

    def post(self, request, *args, **kwargs):

        data = without_keys(request.POST, ['file', 'file2', 'birthday', 'passport_created_date', 'age'])
        rs = RequestPost(Customer.objects.get(id=kwargs['pk']), data)
        customer = rs.set(commit=False)

        if request.FILES.get('file', None) != None:
            customer.file = request.FILES.get('file', '')

        if request.FILES.get('file2', None) != None:
            customer.file2 = request.FILES.get('file2', '')

        if request.POST['birthday']:
            customer.birthday = convert_date(request.POST['birthday'])

        if request.POST['age']:
            customer.age = request.POST['age']

        customer.passport_created_date = convert_date(request.POST['passport_created_date'])

        return redirect('customers') if try_save(request, customer) else redirect('customers-detail', kwargs['pk'])

class StoreView(LoginRequiredMixin, TemplatePattern, StoreContext):
    template_name = 'main/stores.html'

    def post(self, request, *args, **kwargs):

        if request.POST.get('code', '') in [ store.code for store in Store.objects.all() ]:
            messages.error(request, "Bu kodly dükan eýýäm bar ! Haýyş edýäris başga kod düzüň !")
            return redirect('stores')

        data = without_keys(request.POST, ['employees'])
        rs = RequestPost(Store(), data)
        store = rs.set()

        employees = [Employee.objects.get(id=id) for id in request.POST.getlist('employees', '')]
        store.employees.add(*employees)
        store.employees.add(*[employee.id for employee in Employee.objects.filter(status__title='super-admin')])
        store.save()

        return redirect('stores')

    def put(self, request, *args, **kwargs):

        store = Store.objects.get(id=request.POST.get('pk'))

        if request.POST.get('code', '') in [ store.code for store in Store.objects.all() ] and store.code != request.POST.get('code', ''):
            messages.error(request, "Bu kodly dükan eýýäm bar ! Haýyş edýäris başga kod düzüň !")
            return redirect('stores')

        data = without_keys(request.POST, ['employees'])
        rs = RequestPost(Store.objects.get(id=request.POST['pk']), data)
        store = rs.set()

        employees = [Employee.objects.get(id=id) for id in request.POST.getlist('employees', '')] + [employee for employee in Employee.objects.filter(status__title='super-admin')]
        store.employees.set(employees)
        store.save()

        return redirect('stores')

class EmployeeView(LoginRequiredMixin, TemplatePattern, EmployeeContext):
    template_name = 'main/employees.html'

    def post(self, request, *args, **kwargs):

        if request.POST.get('username', '') in [ user.username for user in User.objects.all() ]:
            messages.error(request, "Bu loginli işgär eýýäm bar ! Haýyş edýäris başga login düzüň !")
            return redirect('employees')

        user = User.objects.create_user(
            username = request.POST.get('username', ''),
            password = request.POST.get('password', ''),
            first_name = request.POST.get('first_name', '')
        )
        user.save()

        employee = Employee(
            user = user,
            password_in_text = request.POST.get('password', ''),
            status = Status.objects.get(title=request.POST.get('status', None))
        )
        employee.save()
        return redirect('employees')

    def put(self, request, *args, **kwargs):

        employee = Employee.objects.get(id=request.POST['pk'])

        if request.POST.get('username', '') in [ user.username for user in User.objects.all().exclude(username=employee.user.username) ]:
            messages.error(request, "Bu loginli işgär eýýäm bar ! Haýyş edýäris başga login düzüň !")
            return redirect('employees')

        employee.user.username = request.POST.get('username', '')
        employee.user.first_name = request.POST.get('first_name', '')
        employee.user.set_password(request.POST.get('password_in_text', f'{employee.user.username}password'))
        employee.user.save()
        employee.password_in_text = request.POST.get('password_in_text', f'{employee.user.username}password')
        employee.save()

        return redirect('employees')


class ReportsView(LoginRequiredMixin, TemplatePattern, LoanContext):
    template_name = 'main/reports.html'

    def get_context_data(self, request, *args, **kwargs):
        LoanContext.get_context_data(self, request, *args, **kwargs)
        context = super().get_context_data(request, *args, **kwargs)
        context['employees'] = Employee.objects.all().exclude(user__is_superuser=True)
        store_id = request.session.get('store', request.user.employee.store_set.first().id)

        if store_id == 'Hemmesi':
            context['transactions'] = Transaction.objects.filter(loan__is_draft=False, loan__store__in=[store for store in request.user.employee.store_set.all()]).filter_or_all(**request.GET)
            if request.user.employee.is_worker():
                context['transactions'] = Transaction.objects.filter_or_all(**request.GET).filter(employee=request.user.employee, loan__is_draft=False)
        else:
            context['transactions'] = Transaction.objects.filter(loan__store=store_id, loan__is_draft=False).filter_or_all(**request.GET)
            if request.user.employee.is_worker():
                context['transactions'] = Transaction.objects.filter(loan__store=store_id, loan__is_draft=False).filter_or_all(**request.GET).filter(employee=request.user.employee)

        context['amount'] = sum([ transaction.amount_price for transaction in context['transactions'] ])

        return context

class LoanReportsView(LoginRequiredMixin, TemplatePattern, LoanContext):
    template_name = 'main/loan-reports.html'

    def get_context_data(self, request, *args, **kwargs):
        LoanContext.get_context_data(self, request, *args, **kwargs)
        context = super().get_context_data(request, *args, **kwargs)
        context['employees'] = Employee.objects.all().exclude(user__is_superuser=True)
        store_id = request.session.get('store', request.user.employee.store_set.first().id)

        if store_id == 'Hemmesi':
            context['loans'] = Loan.objects.filter(is_draft=False, store__in=[store for store in request.user.employee.store_set.all()]).filter_date_range(**request.GET)
            if request.user.employee.is_worker():
                context['loans'] = Loan.objects.filter_date_range(**request.GET).filter(employee=request.user.employee, is_draft=False)
        else:
            context['loans'] = Loan.objects.filter(store=store_id, is_draft=False).filter_date_range(**request.GET)
            if request.user.employee.is_worker():
                context['loans'] = Loan.objects.filter(store=store_id).filter_date_range(**request.GET).filter(employee=request.user.employee, is_draft=False)
        context['amount'] = sum([ loan.first_amount_price() for loan in context['loans'] ])

        return context
