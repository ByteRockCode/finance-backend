from collections import OrderedDict
from datetime import date

from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from graphene.test import Client as ClientGraphene

from .models import Expense
from .schema import schema
from .utils import get_deadline


User = get_user_model()


class ExpenseModelsTestCase(TestCase):
    fixtures = [
        'fixtures/users.json',
        'expenses',
    ]

    def setUp(self):
        self.client = Client()

        is_authenticated = self.client.login(username='yohanna', password='ychavez123456')
        assert is_authenticated, 'The client is not logged'

        self.expense = Expense.objects.get(id=1)

    def test_expense_to_string(self):
        user = User.objects.get(id=1)
        description = 'Lorem ipsum'
        amount = 12345
        deadline = '2018-03-01'

        expense = Expense.objects.create(
            creator=user,
            description=description,
            amount=amount,
            deadline=deadline,
        )

        expense_like_string = expense.__str__()

        self.assertEqual(type(expense_like_string), str)

        assert description in expense_like_string
        assert user.__str__() in expense_like_string
        assert str(amount) in expense_like_string

    def test_expense_get_absolute_url(self):
        url = self.expense.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_expense_get_update_url(self):
        url = self.expense.get_update_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_expense_get_delete_url(self):
        url = self.expense.get_delete_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_expense_get_list_url(self):
        url = self.expense.get_list_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class ExpenseSchemaTestCase(TestCase):
    fixtures = [
        'fixtures/users.json',
        'expenses',
    ]

    def test_expenses(self):
        client = ClientGraphene(schema)
        executed = client.execute('''{ expenses { id }}''')

        aux = {
            'data': OrderedDict(
                [(
                    'expenses',
                    [
                        OrderedDict([('id', str(expense.id))]) for expense in Expense.objects.all()
                    ],
                )],
            ),
        }

        assert executed == aux

    def test_expense(self):
        client = ClientGraphene(schema)
        executed = client.execute('''{ expense (id: 1) { description } }''')

        assert executed == {
            'data': {
                'expense': {
                    'description': 'Señora Rosa'
                }
            }
        }


class ExpenseViewsTestCase(TestCase):
    fixtures = [
        'fixtures/users.json',
        'expenses',
    ]

    def setUp(self):
        self.client = Client()

        is_authenticated = self.client.login(username='yohanna', password='ychavez123456')
        assert is_authenticated, 'The client is not logged'

    def test_redirect(self):
        response = self.client.get(f'/expenses/')
        self.assertEqual(response.status_code, 302)

    def test_list(self):
        response = self.client.get(f'/expenses/2018/06/')
        self.assertEqual(response.status_code, 200)

    def test_create_period_december(self):
        deadline = date(2017, 12, 31)
        url = f'/expenses/{deadline.year}/{deadline.month}/crear/'

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'description': 'Lorem ipsum',
            'amount': 12345,
            'is_accomplished': False,
        }

        queryset = Expense.objects.filter(
            amount=data['amount'],
            description=data['description'],
            is_accomplished=data['is_accomplished'],
            deadline=deadline,
        )

        assert not queryset.exists()

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        assert queryset.exists()

    def test_create_period_january(self):
        deadline = date(2018, 1, 31)
        url = f'/expenses/{deadline.year}/{deadline.month}/crear/'
        data = {
            'description': 'Lorem ipsum',
            'amount': 12345,
            'is_accomplished': False,
        }

        queryset = Expense.objects.filter(
            amount=data['amount'],
            description=data['description'],
            is_accomplished=data['is_accomplished'],
            deadline=deadline,
        )

        assert not queryset.exists()

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        assert queryset.exists()

    def test_update(self):
        expense = Expense.objects.get(id=1)
        url = f'/expenses/{expense.id}/'

        data = {
            'id': expense.id,
            'description': f'Lorem ipsum {expense.description}',
            'amount': 12345,
            'is_accomplished': False,
        }

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        expense = Expense.objects.get(id=1)
        self.assertEqual(expense.description, data['description'])

    def test_delete(self):
        expense = Expense.objects.get(id=1)
        url = f'/expenses/{expense.id}/eliminar/'

        data = {
            'id': expense.id,
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.filter(id=expense.id).exists(), False)


class UtilsTestCase(TestCase):

    def test_get_deadline(self):

        assert get_deadline(date(2016, 2, 1)) == date(2016, 2, 29)

        assert get_deadline(date(2018, 1, 1)) == date(2018, 1, 31)
        assert get_deadline(date(2018, 2, 1)) == date(2018, 2, 28)
        assert get_deadline(date(2018, 3, 1)) == date(2018, 3, 31)
        assert get_deadline(date(2018, 4, 1)) == date(2018, 4, 30)
        assert get_deadline(date(2018, 5, 1)) == date(2018, 5, 31)
        assert get_deadline(date(2018, 6, 1)) == date(2018, 6, 30)
        assert get_deadline(date(2018, 7, 1)) == date(2018, 7, 31)
        assert get_deadline(date(2018, 8, 1)) == date(2018, 8, 31)
        assert get_deadline(date(2018, 9, 1)) == date(2018, 9, 30)
        assert get_deadline(date(2018, 10, 1)) == date(2018, 10, 31)
        assert get_deadline(date(2018, 11, 1)) == date(2018, 11, 30)
        assert get_deadline(date(2018, 12, 1)) == date(2018, 12, 31)
