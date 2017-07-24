from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from jsonfield import JSONField

from . import consts


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class DevinoRequest(models.Model):
    api = models.CharField(max_length=64, choices=consts.STATUS_CHOICES)
    data = JSONField(null=True, blank=True)
    dc = models.DateTimeField(auto_now_add=True)


class DevinoError(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    request = models.OneToOneField(DevinoRequest, related_name='devino_error')
    dc = models.DateTimeField(auto_now_add=True)


class DevinoAnswer(models.Model):
    code = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    result = JSONField(null=True, blank=True)
    request = models.OneToOneField(DevinoRequest, related_name='devino_answer')
    dc = models.DateTimeField(auto_now_add=True)
