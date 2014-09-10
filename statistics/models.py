from django.db import models

from courses.models import Partner


class PartnerStats(models.Model):
    money_spent = models.PositiveIntegerField(default=0, blank=False, null=False)
    partner = models.ForeignKey(Partner)

    class Meta:
        verbose_name_plural = 'Partner Stats'

    def __unicode__(self):
        return unicode('{} - {}'.format(self.partner.name, self.money_spent))
