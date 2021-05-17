from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from member.models import Member

@receiver(post_save, sender=Member, dispatch_uid="创建队员之后自动修改用户类型")
def _(sender, instance: Member=None, created=False, **kwargs):
    if created:
        instance.user.role = User.Role.MEMBER
        instance.save()
