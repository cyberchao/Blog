from django.contrib import admin
from .models import Genre


class GenreAdmin(admin.ModelAdmin):
    list_display=('blog', 'name', 'body','timestamp')
admin.site.register(Genre,GenreAdmin)
