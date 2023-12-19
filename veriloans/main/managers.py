from django.db.models.query import QuerySet
from django.db.models import Q
from higgs.helpers import foundated_keys

class CustomerQuerySet(QuerySet):

    def filter_or_all(self, *args, **kwargs):

        if kwargs != {}:
            kwargs = foundated_keys(kwargs)

            customers = self.filter(Q(first_name__icontains=kwargs['client'])|
                                    Q(last_name__icontains=kwargs['client'])|
                                    Q(patronymic__icontains=kwargs['client'])
                                    ).filter(passport_id__icontains=kwargs['passport_id'])

            if kwargs.get('in_blacklist', '') in ['Gara sanawdakylar']:
                customers = customers.filter(in_blacklist=True)
                
            return customers

        return self.all()[:100]

    def serializers(self, *args, **kwargs):
        kwargs = foundated_keys(kwargs)
        return [customer.serializer() for customer in self.filter(Q(first_name__icontains=kwargs['client'])|
                                                                  Q(last_name__icontains=kwargs['client'])|
                                                                  Q(patronymic__icontains=kwargs['client'])|
                                                                  Q(phone__icontains=kwargs['client'])|
                                                                  Q(passport_id=kwargs['client']))]

class StoreQuerySet(QuerySet):

    def filter_or_all(self, *args, **kwargs):

        if kwargs != {}:
            kwargs = foundated_keys(kwargs)

            stores = self.filter(title__icontains=kwargs['title'])
            return stores

        return self.all()


class ProductQuerySet(QuerySet):

    def filter_or_all(self, *args, **kwargs):

        if kwargs != {}:
            kwargs = foundated_keys(kwargs)

            products = self.filter(title__icontains=kwargs['title'])
            return products if not kwargs['category'] else products.filter(category__title=kwargs['category'])

        return self.all()

    def serializers(self, *args, **kwargs):
        kwargs = foundated_keys(kwargs)
        return [product.serializer() for product in self.filter(check_number__icontains=kwargs['check_number'])[:6]]
