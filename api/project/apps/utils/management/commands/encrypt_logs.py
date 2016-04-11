from django.db import transaction
from django.core.management.base import BaseCommand
import json
from binascii import hexlify
from simplecrypt import encrypt
from events.models import Event
from events.tasks import encrypt_event


class Command(BaseCommand):
    help = 'Exports emails for campaigns - temp fix.'

    def add_arguments(self, parser):
        parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        total = Event.objects.count()
        c = 0
        for e in Event.objects.all():
            c += 1
            encrypt_event.delay(e.pk, c, total)
