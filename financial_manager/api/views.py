from django.db.models import Sum
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Transaction
from .serializers import TransactionSerializer
from .permissions import OnlyOwnerHasAccess


class TransactionViewSet(ModelViewSet):
    """
    Lists, retrieves, creates, updates, deletes Transactions,
    related to current authenticated request user.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (OnlyOwnerHasAccess,)
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date', 'amount')

    def get_queryset(self, *args, **kwargs):
        """
        Fetches queryset, provides filtering against url params,
        also checks if 'pk' is passed through router to fetch the specific object.
        """

        queryset = self.queryset.filter(user=self.request.user)
        pk = self.kwargs.get('pk', None)
        date = self.request.query_params.get('date', None)
        params = self.request.query_params.get('type')
        transaction_type = params if params in ('in', 'out') else None

        if pk:
            return queryset.filter(pk=pk)

        elif date and not transaction_type:
            return queryset.filter(date=date)

        elif date and transaction_type == 'in':
            return queryset.filter(date=date, amount__gt=0)

        elif date and transaction_type == 'out':
            return queryset.filter(date=date, amount__lt=0)

        elif not date and transaction_type == 'in':
            return queryset.filter(amount__gt=0)

        elif not date and transaction_type == 'out':
            return queryset.filter(amount__lt=0)

        return queryset

    def perform_create(self, serializer):
        """ Passes 'user' attribute to the serializer. """

        serializer.save(user=self.request.user)


class GetIncomeSumView(APIView):
    """
    Represents sums of INCOMING transactions amounts grouped by dates.
    Also provides 'start date' and 'end date' filtering in it.
    """

    permission_classes = (OnlyOwnerHasAccess,)

    def get(self, request) -> Response:
        start_date = request.query_params.get('start', None)
        end_date = request.query_params.get('end', None)
        transactions = Transaction.objects.filter(
            user=request.user,
            amount__gt=0
        ).values(
            'date'
        ).annotate(
            sum=Sum('amount')
        )

        if start_date and end_date:
            return Response(transactions.filter(date__range=(start_date, end_date)))

        elif start_date and not end_date:
            return Response(transactions.filter(date__gte=start_date))

        elif not start_date and end_date:
            return Response(transactions.filter(date__lte=end_date))

        return Response(transactions)


class GetOutcomeSumView(APIView):
    """
    Represents sums of WITHDRAWAL transactions amounts grouped by dates.
    Also provides 'start date' and 'end date' filtering in it.
    """

    permission_classes = (OnlyOwnerHasAccess,)

    def get(self, request) -> Response:
        start_date = request.query_params.get('start', None)
        end_date = request.query_params.get('end', None)
        transactions = Transaction.objects.filter(
            user=request.user, amount__lt=0
        ).values(
            'date'
        ).annotate(
            sum=Sum('amount')
        )

        if start_date and end_date:
            return Response(transactions.filter(date__range=(start_date, end_date)))

        elif start_date and not end_date:
            return Response(transactions.filter(date__gte=start_date))

        elif not start_date and end_date:
            return Response(transactions.filter(date__lte=end_date))

        return Response(transactions)
