from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)

class EmailConfirmation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)

class Category(models.TextChoices):
    TANKS = "Танки"
    HEALERS = "Хилы"
    DPS = "ДД"
    TRADERS = "Торговцы"
    GUILDMASTERS = "Гилдмастеры"
    QUESTGIVERS = "Квестгиверы"
    BLACKSMITHS = "Кузнецы"
    LEATHERWORKERS = "Кожевники"
    ALCHEMISTS = "Зельевары"
    SPELLMASTERS = "Мастера заклинаний"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=Category.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def excerpt(self):
        return self.content[:200] + '...' if len(self.content) > 200 else self.content

class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CategorySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.CharField(max_length=50, choices=Category.choices)

    class Meta:
        unique_together = ('user', 'category')
