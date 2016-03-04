from django.db import models


class Menu(models.Model):

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        ordering = ['sort']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def has_subitems(self):
        return self.subitems.count() > 0

    TARGET_CHOICES = (
        ('EM', ''),
        ('BL', '_blank'),
        ('SF', '_self'),
        ('PR', '_parent'),
        ('TP', '_top'),
    )

    name = models.CharField(max_length=20)
    link = models.CharField(max_length=255)
    target = models.CharField(max_length=2, choices=TARGET_CHOICES, default='EM')
    sort = models.PositiveIntegerField(default=100)
    level = models.IntegerField(default=0)
    subitems = models.ManyToManyField('self', blank=True)
    for_staff = models.BooleanField(default=False)

    def is_active(self):
        return self.sort > 0
    is_active.admin_order_field = 'sort'
    is_active.boolean = True
    is_active.short_description = 'Is active?'
