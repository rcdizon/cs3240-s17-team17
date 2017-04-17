from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Report(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=200, default='DEFAULT')
    companyPhone = models.CharField(max_length=200, default='DEFAULT')
    companyLocation = models.CharField(max_length=200, default='DEFAULT')
    companyCountry = models.CharField(max_length=200, default='DEFAULT')
    sector = models.CharField(max_length=200, default='DEFAULT')
    industry = models.CharField(max_length=200, default='DEFAULT')
    currentProjects = models.TextField(default='DEFAULT')

    YES = 'Yes'
    NO = 'No'
    ENCRYPTED_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No')
    )
    encrypted = models.CharField(choices=ENCRYPTED_CHOICES, default=NO, max_length=4)
    upload = models.FileField(upload_to='media', default=None, null=True, blank=True)

    PUBLIC = 'Public'
    PRIVATE = 'Private'
    PRIVACY_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private')
    )
    privacy = models.CharField(choices=PRIVACY_CHOICES, default=PUBLIC, max_length=10)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.companyName

class Message(models.Model):
     recipient = models.ForeignKey(User, related_name="recipient")
     sender = models.ForeignKey(User, related_name="sender", null=True)
     textbox = models.TextField(max_length=10000)
     timestamp = models.DateTimeField(default=timezone.now)

     def publish(self):
        self.published_date = timezone.now()
        self.sender = request.user
        self.save()

