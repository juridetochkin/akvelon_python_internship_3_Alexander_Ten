import django_filters


class TransactionsListFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    transaction_type = django_filters.LookupChoiceFilter(
        field_name='amount',
        lookup_choices=(
            'income',
            'outcome',
        )
    )
