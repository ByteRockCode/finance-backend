import graphene
from graphene_django import DjangoObjectType

from .models import Expense


class ExpenseObjectType(DjangoObjectType):
    class Meta:
        model = Expense


class Query(graphene.ObjectType):

    expense = graphene.Field(
        ExpenseObjectType,
        id=graphene.Int(),
    )
    companies = graphene.List(ExpenseObjectType)

    def resolve_companies(self, info):
        return Expense.objects.all()

    def resolve_expense(self, info, **kwargs):
        if 'id' in kwargs:
            return Expense.objects.get(id=kwargs['id'])

        return None


schema = graphene.Schema(query=Query)
