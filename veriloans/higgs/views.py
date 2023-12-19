from higgs.helpers import  get_object_fields
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.exceptions import ImproperlyConfigured
from abc import ABC, abstractmethod

class ViewPattern:

    def __init__(self, request, *args, **kwargs):
        self.request = request

    def dispatch(self, request, *args, **kwargs):
        allowed_methods = ['get', 'post', 'put', 'delete']

        try:
            self.allowed_methods
        except:
            self.allowed_methods = allowed_methods

        if self.request.method.lower() not in self.allowed_methods:
            return HttpResponseNotAllowed(allowed_methods)

        method = getattr(self, self.request.method.lower())

        if self.request.POST.get('_method', ''):
            method = getattr(self, self.request.POST.get('_method', '').lower())

        return method(self.request, *args, **kwargs)

    @classmethod
    def as_view(cls):

        def view(request, *args, **kwargs):
            self = cls(request, *args, **kwargs)
            return self.dispatch(request, *args, **kwargs)

        return view

class ContextBuilder:

    def get_context_data(self, request, *args, **kwargs):
        return kwargs

class TemplateResponseBuilder:

    template_name = None

    def render_to_response(self, request, context, *args, **kwargs):
        return render(request, self.get_template_name(), context)

    def get_template_name(self):

        if self.template_name is None:
            raise ImproperlyConfigured('template_name is not configured')
        else:
            return self.template_name

class RequestPost:

    def __init__(self, object, post, *args, **kwargs):
        self.object = object
        self.post = post

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set(self, commit=True):
        datas = get_object_fields(self.object, self.post)

        for key in datas:
            setattr(self.object, key, self.post.get(key, None))

        if commit == True:
             self.object.save()

        return self.object

class TemplatePattern(TemplateResponseBuilder, ContextBuilder, ViewPattern):

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, *args, **kwargs)
        return self.render_to_response(request, context)

        return redirect('products')
