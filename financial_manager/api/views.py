from django.db.models import Sum
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Transaction
from .serializers import TransactionSerializer
from .permissions import OnlyOwnerOrAdminHasAccess


class TransactionViewSet(ModelViewSet):
    """
    Lists, retrieves, creates, updates, deletes Transactions,
    related to current authenticated user.
    """

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (OnlyOwnerOrAdminHasAccess,)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    filterset_fields = ('date',)
    ordering_fields = ('date', 'amount')

    def get_queryset(self, *args, **kwargs):
        """
        Fetches queryset, provides filtering against url type_param,
        also checks if 'pk' is passed through router to fetch the specific object.
        """

        queryset = self.queryset.filter(user=self.request.user)
        pk = self.kwargs.get('pk', None)
        type_param = self.request.query_params.get('type', None)
        transaction_type = type_param if type_param in ('in', 'out') else None

        if pk:
            return queryset.filter(pk=pk)

        if transaction_type == 'in':
            queryset = queryset.filter(amount__gt=0)
        elif transaction_type == 'out':
            queryset = queryset.filter(amount__lt=0)

        return queryset

    def perform_create(self, serializer):
        """ Calls serializer.save() method with 'user' attribute passed there. """

        serializer.save(user=self.request.user)


class GetIncomeSumView(APIView):
    """
    Represents sums of INCOMING transactions amounts grouped by dates.
    Also provides 'start date' and 'end date' filtering.
    """

    permission_classes = (OnlyOwnerOrAdminHasAccess,)

    def get(self, *args, **kwargs):
        transactions = Transaction.objects.filter(
            user=self.request.user,
            amount__gt=0
        ).values(
            'date'
        ).annotate(
            sum=Sum('amount')
        )
        start_date = self.kwargs.get('start', None)
        end_date = self.kwargs.get('end', None)

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
    Also provides 'start date' and 'end date' filtering.
    """

    permission_classes = (OnlyOwnerOrAdminHasAccess,)

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
