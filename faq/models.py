from django.db import models


class Faq(models.Model):
    title = models.CharField(blank=False, max_length=512)
    text = models.TextField(blank=False)

    def __str__(self):
        return self.title
