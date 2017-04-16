from django.db import models
from django.utils import timezone

## def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  ## return 'user_{0}/{1}'.format(instance.user.id, filename)


class Report(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=200, default='Company Name')
    companyPhone = models.CharField(max_length=200, default='Phone')
    companyLocation = models.CharField(max_length=200, default='Location')
    companyCountry = models.CharField(max_length=200, default='Country')
    sector = models.CharField(max_length=200, default='Sector')
    industry = models.CharField(max_length=200, default='Industry')
    currentProjects = models.TextField(default='Current Projects')
    # files attached ? change reports to company name??
    upload = models.FileField(upload_to='media', default=True)
    # public or private


    # NEED classes for what to do when public/private

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.companyName
