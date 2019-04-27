from posts.models import Users as User
from django.db import models


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField(upload_to='album_logo')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title

    class Meta:
        verbose_name = '专辑'
        verbose_name_plural = verbose_name
        db_table = 'Album'


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=100)
    audio_file = models.CharField(max_length=200)
    ytburl = models.CharField(max_length=200, blank=True)
    length = models.IntegerField()

    def __str__(self):
        return self.song_title

    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = verbose_name
        db_table = 'songs'
