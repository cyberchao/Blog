from django.contrib import admin
from .models import Album, Song


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('user', 'album_title','genre', 'is_favorite')


admin.site.register(Album, AlbumAdmin)


class SongAdmin(admin.ModelAdmin):
    list_display = ('album', 'song_title')


admin.site.register(Song, SongAdmin)
