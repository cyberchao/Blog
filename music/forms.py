from django import forms
from posts.models import Users as User

from .models import Album, Song


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
