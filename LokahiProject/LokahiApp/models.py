from django.db import models
from django.utils import timezone

## def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  ## return 'user_{0}/{1}'.format(instance.user.id, filename)


class Report(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=200, default='DEFAULT')
    companyPhone = models.CharField(max_length=200, default='DEFAULT')
    companyLocation = models.CharField(max_length=200, default='DEFAULT')
    companyCountry = models.CharField(max_length=200, default='DEFAULT')
    sector = models.CharField(max_length=200, default='DEFAULT')
    industry = models.CharField(max_length=200, default='DEFAULT')
    currentProjects = models.TextField(default='DEFAULT')
    # files attached ? change reports to company name??
    YES = 'Yes'
    NO = 'No'
    ENCRYPTED_CHOICES = (
        (YES, 'Yes'),
        (NO, 'No')
    )
    encrypted = models.CharField(choices=ENCRYPTED_CHOICES, default=NO, max_length=4)
    upload = models.FileField(upload_to='media', default=None, null=True, blank=True)
    remove_the_file = models.BooleanField(default=False)
    # public or private


    # NEED classes for what to do when public/private

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.companyName
