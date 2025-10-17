from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from core.models import User

class Command(BaseCommand):
    help = 'Send newsletter to all users'

    def handle(self, *args, **kwargs):
        for user in User.objects.filter(email_confirmed=True):
            send_mail(
                'Новости сервера',
                'Привет! Вот свежие новости сервера...',
                'noreply@mmorpgboard.com',
                [user.email],
                fail_silently=False
            )
        self.stdout.write(self.style.SUCCESS('Newsletter sent successfully'))
