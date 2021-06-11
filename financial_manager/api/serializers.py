from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    """ Serializes transactions. """

    class Meta:
        model = Transaction
        fields = ('id', 'user', 'amount', 'date')
        read_only_fields = ('id', 'user')


class SumSerializer(serializers.ModelSerializer):
    """ Serializes transaction sums. """

    class Meta:
        model = Transaction
        fields = ('amount', 'date')
