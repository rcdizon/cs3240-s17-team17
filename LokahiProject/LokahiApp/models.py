from django.db import models
from django.utils import timezone

## def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
  ## return 'user_{0}/{1}'.format(instance.user.id, filename)


class Report(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    companyName = models.CharField(max_length=200, default='DEFAULT')
    companyPhone = models.CharField(max_length=200)
    companyLocation = models.CharField(max_length=200)
    companyCountry = models.CharField(max_length=200)
    sector = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    currentProjects = models.TextField()
    # files attached ? change reports to company name??
    ## upload = models.FileField(upload_to=user_directory_path)
    # public or private


    # NEED classes for what to do when public/private

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.companyName
