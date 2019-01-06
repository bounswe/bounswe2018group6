from rest_framework import status
from rest_framework.test import APITestCase

from api import views
from api.models import (User)


class LoginTests(APITestCase):
    def setUp(self):
        super(LoginTests, self).setUp()
        self.user = User.objects.create(username='testuser-login',
                                        email='testuser-login@cultidate.com')
        self.user_passive = User.objects.create(username='testuser-login1',
                                                email='testuser-login1@cultidate.com',
                                                is_active=False)
        self.password = 'testpass1923'
        self.user.set_password(self.password)
        self.user_passive.set_password(self.password)
        self.user.save()
        self.user_passive.save()

    def test_login(self):
        """ Tests an active user can login. """
        data = {
            'username': self.user.username,
            'password': self.password
        }
        response = self.client.post('/api/auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user_id'), self.user.pk)
        self.assertEqual(len(response.data.get('token')), 40)

    def test_restrict_login_with_incorrect_password(self):
        """ Test a user cannot login with incorrect password """
        data = {
            'username': self.user.username,
            'password': '{}+'.format(self.password)
        }
        response = self.client.post('/api/auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_for_active_user(self):
        """ Test a passive user cannot login. """
        data = {
            'username': self.user_passive.username,
            'password': self.password
        }
        response = self.client.post('/api/auth/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
