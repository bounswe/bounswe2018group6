from rest_framework import status
from rest_framework.test import APITestCase

from api.models import (User)


class SignupTests(APITestCase):
    def test_signup(self):
        """ Tests if a user can signup. """
        data = {
            'email': 'testusersignup@cultidate.com',
            'username': 'testusersignup',
            'password': '12345678+',
            'first_name': 'name',
            'last_name': 'surname',
            'bio': 'MyBio',
            'city': 'Istanbul',
            'is_corporate_user': False,
            'corporate_profile': None,
        }
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data.pop('id'), int)
        self.assertEqual(response.data.get('email'), data['email'])
        self.assertEqual(response.data.get('username'), data['username'])
        self.assertEqual(response.data.get('first_name'), data['first_name'])
        self.assertEqual(response.data.get('last_name'), data['last_name'])
        self.assertEqual(response.data.get('bio'), data['bio'])
        self.assertEqual(response.data.get('city'), data['city'])
        self.assertEqual(response.data.get('is_corporate_user'), data['is_corporate_user'])
    
    def test_prohibit_with_short_password(self):
        """ Tests if a user can signup with a short password. """
        data = {
            'email': 'testusersignup1@cultidate.com',
            'username': 'testusersignup',
            'password': '1',
            'first_name': 'name',
            'last_name': 'surname',
            'bio': 'MyBio',
            'city': 'Istanbul',
            'is_corporate_user': False,
            'corporate_profile': None,
        }
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_prohibit_with_long_password(self):
        """ Tests if a user can signup with a short password. """
        data = {
            'email': 'testusersignup2@cultidate.com',
            'username': 'testusersignup',
            'password': 'asdfghjkloinhytvbhjgtyuij',
            'first_name': 'name',
            'last_name': 'surname',
            'bio': 'MyBio',
            'city': 'Istanbul',
            'is_corporate_user': False,
            'corporate_profile': None,
        }
        response = self.client.post('/api/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
