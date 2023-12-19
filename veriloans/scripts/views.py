from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Customer, Store
from accounts.models import Employee
from loans.models import Loan, LoanPlan, Transaction
from higgs.helpers import convert_date, convert_date_separately
from dateutil.relativedelta import relativedelta
from datetime import datetime
import csv

# Create your views here.
def import_customers_csv(request):
    with open('csvs/customers.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            customer = Customer(
                first_name=row[0],
                last_name=row[1],
                patronymic=row[2],
                passport_id=row[3],
                age=row[5],
                county=row[12],
                registration=row[10],
                work_place=row[9],
                type=row[13],
                phone=row[6],
                phone2=row[7],
                phone3=row[8],
            )
            customer.birthday = convert_date(row[4])
            customer.passport_created_date = convert_date(row[11])
            customer.save()

    return redirect('index')

def import_loans_csv(request):
    with open('csvs/loans.csv') as f:
        reader = csv.reader(f)
        for row in reader:

            print('---> ', row[7])
            year, month, day = convert_date_separately(row[7])

            loan = Loan(
                store = Store.objects.get(id=row[0]),
                employee = Employee.objects.get(id=row[1]),
                customer = Customer.objects.get(passport_id=row[2]),
                check_numbers = row[3],
                check_numbers_prices = row[4],
                amount_price = row[5],
                amount_month_price = row[6],
                created = datetime(int(year), int(month), int(day)),
            )
            loan.save()

            for i in range(1, 6+1):
                loan_plan = LoanPlan(
                    loan=loan,
                    expiration_time = loan.created + relativedelta(minutes=+i)
                )
                loan_plan.save()

    return redirect('index')



def import_transactions_csv(request):
    with open('csvs/transactions.csv') as f:
        reader = csv.reader(f)

        for row in reader:

            loan = Loan.objects.get(id=row[0])
            request_amount_price = int(row[2])
            indicator = request_amount_price

            start_price_of_indicator = indicator

            while indicator != 0:
                loanplan = LoanPlan.objects.get(id=loan.unpayed_loanplans()[0])

                if indicator > loan.amount_price:
                    return HttpResponse(f"Girizilen töleg algynyň umumy galan töleginden {indicator - loan.amount_price} m geçýär !")

                if indicator >= loan.amount_month_price - loanplan.payment:
                    indicator -= loan.amount_month_price - loanplan.payment
                    loanplan.payment = loan.amount_month_price
                else:
                    loanplan.payment += indicator
                    indicator = 0

                loanplan.save()

            year, month, day = convert_date_separately(row[4])
            transaction = Transaction(
                loan = loan,
                employee = Employee.objects.get(id=row[1]),
                amount_price = request_amount_price,
                type = row[3],
                created = datetime(int(year), int(month), int(day)),
            )
            transaction.save()

            loan.amount_price -= transaction.amount_price
            loan.save()

            if loan.amount_price == 0:
                loan.is_closed = True
                loan.save()
                print(request, f"{loan.customer} müşderiniň {loan.created.strftime('%d-%m-%Y')} senede alan algysy üstünlikli ýapyldy !")

    return redirect('index')
