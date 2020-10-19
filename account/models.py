from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True,null=True)
    photo = CloudinaryField('images',null=True,blank=True)
    def __str__(self):
        return f'Profile for user {self.user.username}'

    class Meta:
        ordering = ['-id']


def userprofile_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=settings.AUTH_USER_MODEL)