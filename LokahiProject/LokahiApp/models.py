from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Report(models.Model):
    author = models.OneToOneField('auth.User')
    timestamp = models.DateField(default=timezone.now)
    companyName = models.CharField(max_length=200, default='')
    companyCEO = models.CharField(max_length=200, default='')
    companyPhone = models.CharField(max_length=200, default='')
    companyLocation = models.CharField(max_length=200, default='')
    companyCountry = models.CharField(max_length=200, default='')
    sector = models.CharField(max_length=200, default='')
    industry = models.CharField(max_length=200, default='')
    currentProjects = models.TextField(default='')

    PUBLIC = 'Public'
    PRIVATE = 'Private'
    PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private')
    )

    privacy = models.CharField(choices=PRIVACY_CHOICES, default=PUBLIC, max_length=10)
    keywords = models.CharField(max_length=200, default='')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.companyName


class Upload(models.Model):
    fileupload = models.FileField(upload_to='media', default=None, null=True, blank=True)
    company = models.ForeignKey(Report, related_name="company")
    YES = 'Yes'
    NO = 'No'
    ENCRYPTED_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No')
    )
    encrypted = models.CharField(choices=ENCRYPTED_CHOICES, default=NO, max_length=4)


class Message(models.Model):
    recipient = models.ForeignKey(User, related_name="recipient")
    sender = models.ForeignKey(User, related_name="sender", null=True)
    encrypted = models.BooleanField(default=True)
    textbox = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(default=timezone.now)

    def set(self,sender,text, encbool):
        self.sender = sender
        self.textbox = text
        self.encrypted = encbool
        self.save()

class Search(models.Model):
	search = models.CharField(max_length=100)

class Private_Key(models.Model):
    priv_key = models.TextField(default='')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public = models.TextField(max_length=2000, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
