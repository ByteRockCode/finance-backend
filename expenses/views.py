from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.generic.base import RedirectView
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.dates import MonthMixin
from django.views.generic.dates import YearMixin
from django.views.generic.dates import _date_from_string


from .models import Expense
from .utils import get_deadline


class ExpenseMixin(YearMixin, MonthMixin):

    def get_date(self):
        return _date_from_string(
            self.get_year(),
            self.get_year_format(),
            self.get_month(),
            self.get_month_format(),
        )

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseMixin, self).get_context_data(*args, **kwargs)

        context['month'] = self.get_date()

        return context


class ExpenseSummaryMixin:

    def get_summary(self):
        queryset = self.object_list

        amount_total = queryset.aggregate(total=Sum('amount')).get('total', 0)

        amount_accomplished = queryset.filter(is_accomplished=True)
        amount_accomplished = amount_accomplished.aggregate(total=Sum('amount')).get('total', 0)

        amount_not_accomplished = queryset.filter(is_accomplished=False)
        amount_not_accomplished = amount_not_accomplished.aggregate(total=Sum('amount'))
        amount_not_accomplished = amount_not_accomplished.get('total', 0)

        return {
            'amount_accomplished': amount_accomplished,
            'amount_not_accomplished': amount_not_accomplished,
            'amount_total': amount_total,
        }

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseSummaryMixin, self).get_context_data(*args, **kwargs)

        context['summary'] = self.get_summary()

        return context


class ExpenseCreateView(LoginRequiredMixin, ExpenseMixin, CreateView):
    model = Expense
    fields = [
        'description',
        'is_accomplished',
        'amount',
    ]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.deadline = get_deadline(self.get_date())

        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_list_url()


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense

    def get_success_url(self):
        return self.object.get_list_url()


class ExpenseRedirectView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'expense-list'

    def get_redirect_url(self, *args, **kwargs):
        today = date.today()

        kwargs['year'] = today.year
        kwargs['month'] = today.month

        return super().get_redirect_url(*args, **kwargs)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        'description',
        'is_accomplished',
        'amount',
    ]
    model = Expense

    def get_context_data(self, *args, **kwargs):
        context = super(ExpenseUpdateView, self).get_context_data(*args, **kwargs)

        context['month'] = self.object.deadline

        return context

    def get_success_url(self):
        return self.object.get_list_url()


class ExpenseMonthArchiveView(LoginRequiredMixin, ExpenseSummaryMixin, MonthArchiveView):
    allow_empty = True
    allow_future = True
    context_object_name = 'expenses'
    date_field = 'deadline'
    model = Expense

    def get_queryset(self):
        queryset = self.model.objects.filter(creator=self.request.user)
        return queryset.order_by('is_accomplished', 'creation_timestamp')
