from .models import ImageUploader


def my_cron_job():
    ImageUploader.objects.all().delete()
