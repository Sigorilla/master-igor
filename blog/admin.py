from django.contrib import admin
from blog.models import Post

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  fieldsets = [
    ("Create new post",   {'fields': ['title', 'intro']}),
    ("More information",  {'fields': ['post', 'tags'], 'classes': ['collapse']}),
  ]
  list_display = ('title', 'pub_date', 'was_published_recently')
  list_filter = ['pub_date']
  search_fields = ['title', 'intro']
  readonly_fields = ('pub_date',)

admin.site.register(Post, PostAdmin)
