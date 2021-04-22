from django.contrib.auth.models import User
from django.db import models
from backend_roc.utils.choice import USER_TYPES
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


def directory_path(instance, filename):
    # print(f"{instance.id} # {instance.user.id}")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return "profile/{}".format(filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15, null=True, unique=True)
    user_type = models.CharField(choices=USER_TYPES,
                                 max_length=10,
                                 null=False)
    profile_image = models.FileField(upload_to=directory_path, default='profile/avatar.jpg')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
