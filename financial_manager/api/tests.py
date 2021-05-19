import requests
from django.test import TestCase, Client
from django.urls import reverse


class RegistrationMixin:
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

    def register_and_get_token(self) -> None:
        """
        Register both users and fills self.token_1 and self.token_2 attributes

        """

        # Login and get token for User 1
        self.client.post(reverse('user-list'), data={
            'first_name': self.first_name_1,
            'last_name': self.last_name_1,
            'email': self.email_1,
            'password': self.password_1,
        })
        response = self.client.post(reverse('login'),
                                    data={'email': self.email_1, 'password': self.password_1})
        self.token_1 = f"Token {response.json()['auth_token']}"

        # Login and get token for User 2
        self.client.post(reverse('user-list'), data={
            'first_name': self.first_name_2,
            'last_name': self.last_name_2,
            'email': self.email_2,
            'password': self.password_2,
        })
        response = self.client.post(reverse('login'),
                                    data={'email': self.email_2, 'password': self.password_2})
        self.token_2 = f"Token {response.json()['auth_token']}"


class TestUser(RegistrationMixin, TestCase):

    updated_first_name = 'Updated First'
    updated_last_name = 'Updated Last'
    updated_email = 'Updated@user.com'
    updated_password = 'UpdLpnmH5975'

    def setUp(self):
        self.register_and_get_token()

    def test_user_get(self):
        url = reverse('user-me')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.token_1)
        self.assertContains(response, self.first_name_1 and self.last_name_1 and self.email_1)

    def test_user_cannot_get_another(self):
        url = reverse('user-me')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.token_1)
        self.assertNotContains(response, self.first_name_2 and self.last_name_2 and self.email_2)

    def test_user_update(self):
        url = reverse('user-me')
        update_data = {
            'first_name': self.updated_first_name,
            'last_name': self.updated_last_name,
        }
        response = self.client.put(
            url, data=update_data, content_type='application/json', HTTP_AUTHORIZATION=self.token_1)
        self.assertContains(response, self.updated_first_name and self.updated_last_name)

    def test_user_email_update(self):
        url = reverse('user-set-username')
        data = {
            'current_password': self.password_1,
            'new_email': self.updated_email
        }
        response = self.client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self.token_1,
            HTTP_ACCEPT='application/json')
        self.assertTrue(response.status_code, 204)

    def test_user_password_update(self):
        url = reverse('user-set-password')
        data = {
            'current_password': self.updated_password,
            'new_password': self.password_1
        }
        response = self.client.post(
            url,
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self.token_1,
            HTTP_ACCEPT='application/json')
        self.assertTrue(response.status_code, 204)


