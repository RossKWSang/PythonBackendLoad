import json
from urllib.request import urlopen

from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hottrack.models import Song


def index(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("query", "").strip()

    song_qs: QuerySet = Song.objects.all()

    if query:
        song_qs = song_qs.filter(
            Q(name__icontains=query) |
            Q(artist_name__icontains=query) |
            Q(album_name__icontains=query)
        )

    return render(
        request=request,
        template_name="hottrack/index.html",
        context={
            "song_list": song_qs,
            "query": query,
        },
    )
