from django.test import RequestFactory
from model_mommy import mommy
from rest_framework import status
from rest_framework.test import (APIClient, APITestCase, force_authenticate)

from api.models import *
from api.views import *


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


class EventTest(APITestCase):
    def setUp(self):
        self.user1 = mommy.make(User, id=1, email='abc@def.com')
        self.artist = mommy.make(User, id=2, email='xyz@uvw.com')
        self.user2 = mommy.make(User, id=3, email='klm@def.com')
        self.user3 = mommy.make(User, id=4, email='qwe@rty.com')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
        self.anonymous_client = APIClient()

        self.tag1 = mommy.make(Tag, id=1)
        self.tag2 = mommy.make(Tag, id=2)

        self.event1 = mommy.make(Event, id=1, owner=self.user1)
        self.event2 = mommy.make(Event, id=2, owner=self.user2)

    def test_get_list_of_events(self):
        response = self.client.get('/api/events_list/')
        self.assertEqual(len(response.data), 2)

    def test_create_event_fails_without_authentication(self):
        response = self.anonymous_client.post('/api/events/', data={}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_event_fails_without_required_fields(self):
        data = {
            "artists": [2],
            "tags": [1, 2]
        }
        response = self.client.post('/api/events/', data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('title' in response.data)
        self.assertTrue('description' in response.data)
        self.assertTrue('location' in response.data)

    def test_create_event_fails_with_not_existing_related_objects(self):
        data = {
            "title": "Cultidate Party",
            "description": "Will be super fun...",
            "date": "2018-11-11T14:00:00Z",
            "artists": [3],
            "tags": [3]
        }
        response = self.client.post('/api/events/', data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('artists' in response.data)
        self.assertTrue('tags' in response.data)

    def test_event_can_be_edited_only_by_owner(self):
        response = self.client.put('/api/events/2/', data={}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_edit_required_fields_of_event(self):
        data = {
            "title": "Art Istanbul"
        }
        response = self.client.put('/api/events/1/', data=data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Art Istanbul')


class EventRelatedActionsTest(APITestCase):
    def setUp(self):
        self.user1 = mommy.make(User, id=1, email='abc@def.com')
        self.user2 = mommy.make(User, id=2, email='klm@def.com')
        self.user3 = mommy.make(User, id=3, email='qwe@rty.com')

        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)
        self.client2 = APIClient()
        self.client2.force_authenticate(user=self.user2)
        self.client3 = APIClient()
        self.client3.force_authenticate(user=self.user3)

        self.event1 = mommy.make(Event, id=1, owner=self.user1)
        self.event2 = mommy.make(Event, id=2, owner=self.user2)

    def test_follower_is_added(self):
        data = {
            'content_type': 'event',
            'object_id': 2
        }
        response = self.client1.post('/api/follow/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.event2.followers.count(), 1)

    def test_vote_is_added(self):
        data = {
            'content_type': 'event',
            'object_id': 2,
            'vote': 'D'
        }
        response = self.client1.post('/api/vote/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.event2.votes.count(), 1)
        self.assertEqual(self.event2.votes.first().vote_value, -1)

    def test_attendance_is_added(self):
        data = {
            'event': 2,
            'status': 'M'
        }
        response = self.client1.post('/api/attendance/', data=data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.event2.attendance_status.count(), 1)
        self.assertEqual(self.event2.attendance_status.first().status, 'M')


class AnnotationTest(APITestCase):
    def setUp(self):
        self.user1 = mommy.make(User, id=1, email='abc@def.com')

        self.client1 = APIClient()
        self.client1.force_authenticate(user=self.user1)

        self.event1 = mommy.make(Event, id=1)

    def test_annotation_should_comply_with_W3C(self):
        data = {
            "content_type": "event",
            "object_id": 1,
            "data": {}
        }
        response = self.client1.post('/api/annotations/', data=data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue('@context' in response.data['missing_fields'])
        self.assertTrue('id' in response.data['missing_fields'])
        self.assertTrue('type' in response.data['missing_fields'])
        self.assertTrue('body' in response.data['missing_fields'])
        self.assertTrue('target' in response.data['missing_fields'])

    def test_annotations_correct_handling(self):
        data = {
            "content_type": "event",
            "object_id": 1,
            "data": {
                "@context": "http://www.w3.org/ns/anno.jsonld",
                "id": "http://example.org/anno1",
                "type": "Annotation",
                "body": "http://example.org/post1",
                "target": "http://example.com/page1"
            }
        }
        response = self.client1.post('/api/annotations/', data=data, format='json')
        self.assertEqual(response.status_code, 201)