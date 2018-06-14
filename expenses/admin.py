from django.contrib import admin

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'amount',
        'deadline',
    )


admin.site.register(Expense, ExpenseAdmin)
