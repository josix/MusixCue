from django.shortcuts import render
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from music.models import Song, Album, Artist, Release, BelongTo
# Create your views here.

def search(request):
    song, album, artist = request.GET['song'], request.GET['album'], request.GET['artist']

    song_like = "%%" if song == "" else "%%{}%%".format(song)
    artist_like = "%%" if artist == "" else "%%{}%%".format(artist)
    album_like = "%%" if album == "" else "%%{}%%".format(album)
    sql = "select * from music_song as SONG \
                INNER JOIN music_belongto as BLON \
                    on SONG.SongID = BLON.SongID_id \
                INNER JOIN music_album as ALB \
                    on BLON.AlbumID_id = ALB.AlbumID \
                INNER JOIN music_release as REL \
                    on ALB.AlbumID = REL.AlbumID_id \
                INNER JOIN music_artist as ART \
                    on REL.ArtistID_id = ART.ArtistID \
            WHERE \
                SONG.SongName LIKE \"{}\" AND \
                ALB.AlbumName LIKE \"{}\" AND \
                ART.ArtistName LIKE \"{}\" ".format(song_like, album_like, artist_like)

    songs = Song.objects.raw(sql)

    ls_return = []
    for s in songs:
        entry_tmp = "SongName: {}, AlbumName: {}, ArtistName: {}".format(s.SongName, s.AlbumName, s.ArtistName)
        print(entry_tmp)
        ls_return.append(entry_tmp)

    #return HttpResponse("song = {}, album = {}, artist = {}".format(song, album, artist) )
    return HttpResponse( ls_return )

def index(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'index.html', locals())

# User's playlist
def playlist(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'playlist.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")

def comment(request):
    if request.user.is_authenticated():
        if request.method == 'GET':
            return render(request, 'comment.html', locals())
    else:
        return HttpResponseRedirect("/accounts/login/")
