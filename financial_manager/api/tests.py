import requests
from django.test import TestCase, Client
from django.urls import reverse


class RegistrationMixin(TestCase):
    first_name_1 = 'First1'
    last_name_1 = 'Last1'
    email_1 = 'test1@user1.com'
    password_1 = 'LpnmH5975'
    token_1 = ''

    first_name_2 = 'First2'
    last_name_2 = 'Last2'
    email_2 = 'test2@user2.com'
    password_2 = 'LpnmH5975'
    token_2 = ''

    client = Client()

    def test_registration(self):
        """ Getting tokens for both users """

        # Login and get token for User 1
        self.client.post(reverse('user-list'), data={
            'first_name': self.first_name_1,
            'last_name': self.last_name_1,
            'email': self.email_1,
            'password': self.password_1,
        })
        response = self.client.post(reverse('login'), data={'email': self.email_1, 'password': self.password_1})
        self.token_1 = f"Token {response.json()['auth_token']}"

        # Login and get token for User 2
        self.client.post(reverse('user-list'), data={
            'first_name': self.first_name_2,
            'last_name': self.last_name_2,
            'email': self.email_2,
            'password': self.password_2,
        })
        response = self.client.post(reverse('login'), data={'email': self.email_2, 'password': self.password_2})
        self.token_2 = f"Token {response.json()['auth_token']}"


# class TestTransactions(RegistrationMixin, TestCase):
#
#     def test_transaction_create(self):
#         self.assertTrue()


