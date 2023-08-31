from django.core.management import BaseCommand
from training.models import Payments


class Command(BaseCommand):
    """����� �������, ������� ������ �� ���� ������, ����� ��� ���������"""

    def handle(self, *args, **options):

        payment_list = [
            {
             'date_payment': '2022-10-01',
             'payment_amount': 86000,
             'payment_method': '������� �� ����',
             'is_paid': True },

            {
             'date_payment': '2022-11-10',
             'payment_amount': 85000,
             'payment_method': '��������',
             'is_paid': True },
        ]

        payments_objects = []
        for payments_item in payment_list:
            payments_objects.append(Payments(**payments_item))

        Payments.objects.bulk_create(payments_objects)