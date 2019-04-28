from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm
from .models import Album, Song
import json
from mutagen.mp3 import MP3

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        albums = Album.objects.filter(user=request.user)
        song_results = Song.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_title__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {
                'albums': albums,
                'songs': song_results,
            })
        else:
            return render(request, 'music/index.html', {'albums': albums})


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/create_album.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)
        mp3 = MP3(song.audio_file)
        song.length = round(mp3.info.length)
        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


"""
{
    title: 'Lost On You',
    duration: 268,
    album: {
        title: 'Lost On You',
        art: {
            square: 'https://images.genius.com/bacae5471acb7b1a4ef445c92e049848.1000x1000x1.jpg',                    }
    },
    url: `${archiveBase}/LostOnYou_201610/Lost On You.mp3`
}
"""


def detail(request, album_id):
    playlist = []
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        songs = Song.objects.filter(album=album)
        for song in songs:
            song = {'title': song.song_title.strip('music/').split('.')[0],
                    'duration': song.length,
                    "album": {
                        'title': song.album.album_title,
                        'art': {
                            'square': album.album_logo.url,
                        }},
                    'url': song.audio_file,
                    # 'ytburl': song.ytburl
                    }
            playlist.append(song)
        jsonlist = json.dumps(playlist, ensure_ascii=False)
        return render(request, 'music/detail.html', {
            'album': album,
            'playlist': jsonlist,
        })
        # return render(request, 'music/detail.html', {'album': album, 'user': user})


# def favorite(request, song_id):
#     song = get_object_or_404(Song, pk=song_id)
#     try:
#         if song.is_favorite:
#             song.is_favorite = False
#         else:
#             song.is_favorite = True
#         song.save()
#     except (KeyError, Song.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})
#
#
# def favorite_album(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         if album.is_favorite:
#             album.is_favorite = False
#         else:
#             album.is_favorite = True
#         album.save()
#     except (KeyError, Album.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})


def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
