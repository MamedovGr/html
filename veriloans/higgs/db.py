from django.db import IntegrityError
from django.core.exceptions import ValidationError
from main.models import *
from accounts.models import *
from django.contrib import messages

def dict_of_errors():
    return {
        'UNIQUE constraint failed: main_customer.passport_id': 'Bu passport seriýaly müşderi eýýäm bar !',
    }

def try_save(request, object, result=False):

    try:
        object.save(); result = True
        messages.success(request, "Üstünlikli amala aşyryldy !")
    except ValidationError:
        messages.error(request, "Sene nädogry formatda girizilen !")
    except Exception as e:
        messages.error(request, dict_of_errors().get(str(e), 'Bu passport seriýaly müşderi eýýäm bar !'))

    return result
