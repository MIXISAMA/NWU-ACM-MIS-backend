from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from user.models import User

@receiver(post_save, sender=User, dispatch_uid="创建用户之后要自动生成令牌")
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=User, dispatch_uid="创建用户之后自动生成头像")
def _(sender, instance:User=None, created=False, **kwargs):
    if created:
        instance.generate_avatar()
