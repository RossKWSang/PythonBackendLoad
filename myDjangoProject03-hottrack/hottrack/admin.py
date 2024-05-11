from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Song

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ["name", "artist_name", "album_name"]
    list_display = [
        "cover_image",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    list_filter = ["genre", "release_date"]

    @staticmethod
    def cover_image(song) -> str:
        return format_html(
'<img src="{}" style="width: 50px; height: 50px;">', song.cover_url
        )
