from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


User = get_user_model()


class Expense(models.Model):
    creator = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)

    description = models.TextField()
    amount = models.IntegerField(validators=[MinValueValidator(1)])

    deadline = models.DateField()
    is_accomplished = models.BooleanField(default=False)

    creation_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'expenses'

    def __str__(self):
        return f'{self.creator} debe gastar ${self.amount} por concepto de {self.description}'

    def get_absolute_url(self):
        return self.get_update_url()

    def get_update_url(self):
        return reverse('expense-update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('expense-delete', kwargs={'pk': self.pk})

    def get_list_url(self):
        kwargs = {
            'year': self.deadline.year,
            'month': self.deadline.month,
        }

        return reverse('expense-list', kwargs=kwargs)
