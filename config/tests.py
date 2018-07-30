from datetime import date

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client


class IndexTestCase(StaticLiveServerTestCase):
    fixtures = [
        'fixtures/users',
    ]

    def test_render_landing_when_unauthenticated(self):
        client = Client()
        response = client.get('/')

        self.assertEqual(response.status_code, 200)

    def test_redirect_to_expenses_when_authenticated(self):
        client = Client()
        client.login(username='juanperez', password='jperez123456')
        response = client.get('/')

        today = date.today()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/expenses/{today.year}/{today.month}/')
