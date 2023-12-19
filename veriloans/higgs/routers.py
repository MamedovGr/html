from django.urls import path
from main import views
import sys, inspect

def get_classes(app_name, model_name) -> dict:
    view_list = {}

    for name, obj in inspect.getmembers(sys.modules[f'{app_name}.views']):
        if inspect.isclass(obj):
            if obj.__name__.startswith(model_name.title()) and obj.__name__.endswith('View'):
                try:
                    view_list[name] = obj
                except:
                    pass

    return view_list


class SimpleRouter:

    def __init__(self, app_name):
        self.app_name = app_name
        self.urls = []

    def collect(self, model_name, view_list) -> None:

        try:
            self.urls += [path(f'{model_name}/', view_list[f'{model_name[:-1].title()}View'].as_view(), name=f'{model_name}')]
        except KeyError:
            pass

        try:
            self.urls += [path(f'{model_name}/create', view_list[f'{model_name[:-1].title()}CreateView'].as_view(), name=f'{model_name}-create')]
        except KeyError:
            pass

        try:
            self.urls += [path(f'{model_name}/<int:pk>/', view_list[f'{model_name[:-1].title()}DetailView'].as_view(), name=f'{model_name}-detail')]
        except KeyError:
            pass


        try:
            self.urls += [path(f'{model_name}/update/<int:pk>/', view_list[f'{model_name[:-1].title()}UpdateView'].as_view(), name=f'{model_name}-update')]
        except KeyError:
            pass

        try:
            self.urls += [path(f'{model_name}/delete/<int:pk>/', view_list[f'{model_name[:-1].title()}DeleteView'].as_view(), name=f'{model_name}-delete')]
        except KeyError:
            pass


    def register(self, model_name) -> None:
        self.collect(model_name, get_classes(self.app_name, model_name[:-1]))
