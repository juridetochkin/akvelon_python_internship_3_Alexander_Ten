from django_filters import rest_framework as filters
from .models import Transaction


class TransactionsFilter(filters.FilterSet):
    """
    Class, configuring django-filters filtering feature
    """

    date = filters.DateFilter(field_name='date', lookup_expr='exact')

    class Meta:
        model = Transaction
        fields = ('date',)
