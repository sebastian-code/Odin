from django.db import models


# Create your models here.
class Faq(models.Model):
    title = models.CharField(blank=False, max_length=512)
    text = models.TextField(blank=False)

    def __unicode__(self):
        return self.title
