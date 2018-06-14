from django.urls import path

from .views import ExpenseCreateView
from .views import ExpenseDeleteView
from .views import ExpenseUpdateView
from .views import ExpenseRedirectView
from .views import ExpenseMonthArchiveView


urlpatterns = [
    path('', ExpenseRedirectView.as_view(), name='expense-redirect'),

    path(
        '<int:year>/<int:month>/crear/',
        ExpenseCreateView.as_view(month_format='%m'),
        name='expense-create',
    ),

    path(
        '<int:year>/<int:month>/',
        ExpenseMonthArchiveView.as_view(month_format='%m'),
        name='expense-list',
    ),

    path(
        '<int:pk>/',
        ExpenseUpdateView.as_view(),
        name='expense-update',
    ),

    path(
        '<int:pk>/eliminar',
        ExpenseDeleteView.as_view(),
        name='expense-delete',
    ),
]
