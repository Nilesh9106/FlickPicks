from django.contrib import admin
from .models import Movie,Favorite,WatchHistory
# Register your models here.
admin.site.register(Favorite)
admin.site.register(WatchHistory)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_date",'spoken_languages')
    list_filter = ("status","spoken_languages")
    search_fields = ("title",)

admin.site.site_header = "FlickPicks"
admin.site.site_title = "FlickPicks Admin Portal"
admin.site.index_title = "Welcome to FlickPicks Portal"