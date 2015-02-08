from django.contrib import admin
from menu.models import Menu

class MenuAdmin(admin.ModelAdmin):
  '''
    Admin View for Menu
  '''
  list_display = ('name', 'sort', 'target', 'is_active')
  list_filter = ('sort',)
  search_fields = ['name', 'link']

admin.site.register(Menu, MenuAdmin)
