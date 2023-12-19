def import_models() -> None:
    from django.contrib.auth.models import User
    from main.models import Store, Category, Product, Customer
    from accounts.models import Employer

def import_higgs_tools() -> None:
    from higgs.helpers import without_keys, convert_date, get_object_fields
    from higgs.db import try_save
    from higgs.views import BasePattern, RequestPost, TemplatePattern

def import_django_tools() -> None:
    from django.shortcuts import render, redirect
    from django.http import HttpResponse
    from django.contrib.auth.mixins import LoginRequiredMixin

def import_exceptions() -> None:
    from django.core.exceptions import ImproperlyConfigured
