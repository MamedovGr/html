from .models import Store, Customer
from higgs.views import ContextBuilder
from django.contrib.auth.models import User
from accounts.models import Employee, Status
from loans.models import Loan, Transaction
from main.models import Store
from datetime import datetime
from django.shortcuts import redirect

class IndexContext(ContextBuilder):

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)

        # context['store'] = Store.objects.get(id=request.session.get('store'))

        store_id = request.session.get('store', request.user.employee.store_set.first().id)

        if store_id == 'Hemmesi':
            context['sum_of_loans_amount'] = sum([ loan.first_amount_price() for loan in Loan.objects.filter(is_draft=False) ])
            context['sum_of_loans_amount_payed'] = sum([ loan.payed_amount_summary() for loan in Loan.objects.filter(is_draft=False) ])
            context['sum_of_loans_amount_unpayed'] = sum([ loan.amount_price for loan in Loan.objects.filter(is_draft=False) ])

            context['todays_sum_of_loans_amount'] = sum([ loan.first_amount_price() for loan in Loan.objects.filter(is_draft=False, created__startswith=datetime.today().strftime('%Y-%m-%d')) ])
            context['todays_sum_of_transactions'] = sum([ transaction.amount_price for transaction in Transaction.objects.filter(created__startswith=datetime.today().strftime('%Y-%m-%d')) if transaction.loan.is_draft == False ])
            context['until_todays_sum_of_loans_amount_unpayed'] = sum([ loan.only_lated_unpayed_loanplans_amount() for loan in Loan.objects.filter(is_draft=False, is_closed=False) if loan.next_expiration_time().strftime('%Y-%m-%d %H:%i:%s') < datetime.now().strftime('%Y-%m-%d %H:%i:%s') ])
        else:
            context['sum_of_loans_amount'] = sum([ loan.first_amount_price() for loan in Loan.objects.filter(is_draft=False) if loan.store.id == store_id ])
            context['sum_of_loans_amount_payed'] = sum([ loan.payed_amount_summary() for loan in Loan.objects.filter(is_draft=False) if loan.store.id == store_id ])
            context['sum_of_loans_amount_unpayed'] = sum([ loan.amount_price for loan in Loan.objects.filter(is_draft=False) if loan.store.id == store_id ])

            context['todays_sum_of_loans_amount'] = sum([ loan.first_amount_price() for loan in Loan.objects.filter(is_draft=False, created__startswith=datetime.today().strftime('%Y-%m-%d')) if loan.store.id == store_id ])
            context['todays_sum_of_transactions'] = sum([ transaction.amount_price for transaction in Transaction.objects.filter(created__startswith=datetime.today().strftime('%Y-%m-%d')) if transaction.loan.store.id == store_id and transaction.loan.is_draft == False])
            context['until_todays_sum_of_loans_amount_unpayed'] = sum([ loan.only_lated_unpayed_loanplans_amount() for loan in Loan.objects.filter(is_draft=False, is_closed=False) if loan.next_expiration_time().strftime('%Y-%m-%d %H:%i:%s') < datetime.now().strftime('%Y-%m-%d %H:%i:%s') and loan.store.id == store_id ])


        return context

class CustomerContext(ContextBuilder):

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        context['customers'] = Customer.objects.filter_or_all(**request.GET)

        return context

class StoreContext(ContextBuilder):

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        context['stores'] = Store.objects.filter_or_all(**request.GET)
        context['employees'] = Employee.objects.workers()

        return context

class EmployeeContext(ContextBuilder):

    def get_context_data(self, request, *args, **kwargs):
        context = super().get_context_data(request, *args, **kwargs)
        context['employees'] = Employee.objects.filter_or_all(**request.GET).exclude(user__is_superuser=True)
        context['statuses'] = Status.objects.all().exclude(title='super-admin')

        return context
