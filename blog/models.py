from django.db import models
import datetime
from django.utils import timezone
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    intro = models.TextField()
    post = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
