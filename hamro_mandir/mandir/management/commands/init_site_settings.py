from django.core.management.base import BaseCommand
from mandir.models import SiteSettings

class Command(BaseCommand):
    help = 'Initialize site settings if they don\'t exist'

    def handle(self, *args, **kwargs):
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create()
            self.stdout.write(self.style.SUCCESS('Successfully created site settings'))
        else:
            self.stdout.write(self.style.WARNING('Site settings already exist'))