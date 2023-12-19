from django.shortcuts import render, redirect
from .models import Store, Customer
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
from loans.models import Transaction, Loan
from datetime import datetime
import xlwt

def switch_store(request, pk):
    request.session['store'] = pk
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def switch_store_to_all(request):
    request.session['store'] = 'Hemmesi'
    return redirect(request.META.get('HTTP_REFERER', 'index'))

def customer_lock_toggle(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.editable = not customer.editable
    customer.save()
    return redirect('customers')

def customer_blacklist_toggle(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.in_blacklist = not customer.in_blacklist
    customer.save()
    return redirect('customers')

def customer_lock_query(request):
    Customer.objects.filter_or_all(**request.GET).update(editable=False)
    return redirect(reverse('customers') + f"?client={ request.GET['client'] }&passport_id={ request.GET['passport_id'] }")

def customer_unlock_query(request):
    Customer.objects.filter_or_all(**request.GET).update(editable=True)
    return redirect(reverse('customers') + f"?client={ request.GET['client'] }&passport_id={ request.GET['passport_id'] }")

def export_reports_xls(request, *args, **kwargs):
    store_id = request.session.get('store', request.user.employee.store_set.first().id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="töleg-hasabat({datetime.today()}).xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Töleg Hasabat')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Şertnama', 'Müşderi', '	Töleg geçiren işgär', 'Geçirilen töleg', 'Töleg görnüşi', 'Geçirilen wagty']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    if store_id != 'Hemmesi':
        transactions = [ transaction for transaction in Transaction.objects.filter_or_all(**request.GET) if transaction.loan.is_draft == False and transaction.loan.store.id == store_id ]
    else:
        transactions = [ transaction for transaction in Transaction.objects.filter_or_all(**request.GET) if transaction.loan.is_draft == False ]

    rows = [(
            str(transaction.loan.get_id()),
            str(transaction.loan.customer),
            str(transaction.employee.user.first_name),
            str(transaction.amount_price),
            str(transaction.type),
            str(transaction.created.strftime('%d-%m-%Y'))
            )
            for transaction in transactions ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])

    wb.save(response)

    return response

def export_loans_xls(request, *args, **kwargs):
    store_id = request.session.get('store', request.user.employee.store_set.first().id)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="algy-hasabat({datetime.today()}).xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Algy Hasabat')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Şertnama', 'Müşderi', 'Telefon', 'Möçberi', 'Alan wagty']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    if store_id != 'Hemmesi':
        loans = Loan.objects.filter(is_draft=False).filter(store = store_id).filter_date_range(**request.GET)
    else:
        loans = Loan.objects.filter(is_draft=False).filter_date_range(**request.GET)

    rows = [(
            str(loan.get_id()),
            str(loan.customer),
            str(loan.customer.phone),
            str(loan.first_amount_price()),
            str(loan.created.strftime('%d-%m-%Y'))
            )
            for loan in loans ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])

    wb.save(response)

    return response
