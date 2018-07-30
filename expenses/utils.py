from datetime import timedelta


def get_deadline(date):
    if date.month == 12:
        deadline = date.replace(year=date.year + 1, month=1) - timedelta(days=1)

    else:
        deadline = date.replace(month=date.month + 1) - timedelta(days=1)

    return deadline
