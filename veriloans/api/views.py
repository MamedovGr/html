from django.http import JsonResponse
from main.models import Store, Customer
from accounts.models import Employee
from loans.models import Loan
from higgs.views import RequestPost
import json
from django.views.decorators.csrf import csrf_exempt

def customers(request):
    customers = Customer.objects.serializers(**request.GET)
    return JsonResponse(customers, safe=False)


def store(request, id):
    store = Store.objects.get(id=id)
    data = store.serializer()
    return JsonResponse(data, safe=False)

def employee(request, id):
    employee = Employee.objects.get(id=id)
    data = employee.serializer()
    return JsonResponse(data, safe=False)

def loan(request, id):
    loan = Loan.objects.get(id=id)
    data = loan.serializer()
    return JsonResponse(data, safe=False)



from django.core.paginator import Paginator

def get_paginator_result(
    object_list,
    page: int = 1,
    page_size: int = 25,
):

    paginator = Paginator(object_list, page_size)
    paginated_list = paginator.get_page(page)

    return {
        "object_list": paginated_list,
        "count": paginated_list.paginator.count,
        "page": page,
        "page_size": page_size,
        "total_pages": paginated_list.paginator.num_pages,
        "next_page_number": paginated_list.next_page_number() if paginated_list.has_next() else None,
        "previous_page_number": paginated_list.previous_page_number() if paginated_list.has_previous() else None,
    }




@csrf_exempt
def get_loans_by_passport(request):
    try:
        passport_serial = request.GET.get('passport_serial', '')
        passport_number = request.GET.get('passport_number', '')
    except:
        data = {
            'success': False,
            'data': 'Technical difficulites',
        }
        return JsonResponse(data, safe=False)

    try:
        customer = Customer.objects.get(passport_id=f'{passport_serial} {passport_number}')
    except Exception as e:
        data = {
            'success': False,
            'data': f'{request.GET}',
        }
        return JsonResponse(data, safe=False)

    try:
        page_size = request.GET.get('page_size', 25)
        page = request.GET.get('page', 1)

        loans = Loan.objects.filter(
            customer=customer,
            is_draft=False,
            is_closed=False,
        )

        paginated_loans = get_paginator_result(
            loans,
            page,
            page_size,
        )

        paginated_loans['object_list'] = [ 
            loan.details_for_mobile()
            for loan in paginated_loans['object_list'] 
        ]

        data = {
            'success': True,
            'data': paginated_loans,
        }

    except Exception as e:
        data = {
            'success': False,
            'data': str(e),
        }

    return JsonResponse(data, safe=False)


@csrf_exempt
def get_loans_with_details(request):

    try:
        page_size = request.GET.get('page_size', 25)
        page = request.GET.get('page', 1)

        loans = Loan.objects.filter(
            is_draft=False,
            is_closed=False,
        )

        paginated_loans = get_paginator_result(
            loans,
            page,
            page_size,
        )

        paginated_loans['object_list'] = [ 
            loan.details_for_mobile()
            for loan in paginated_loans['object_list'] 
        ]

        data = {
            'success': True,
            'data': paginated_loans,
        }

    except Exception as e:
        data = {
            'success': False,
            'data': str(e),
        }
    return JsonResponse(data, safe=False)
