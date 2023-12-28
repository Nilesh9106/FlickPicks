from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255,unique=True)
    vote_average = models.FloatField(blank=True,null=True)
    status = models.CharField(max_length=50)
    release_date = models.DateField(blank=True,null=True)
    revenue = models.IntegerField(null=True,blank=True)
    runtime = models.IntegerField(null=True,blank=True)
    credit = models.CharField(max_length=255,null=True,blank=True)
    budget = models.IntegerField(null=True,blank=True)
    overview = models.TextField()
    popularity = models.FloatField(null=True,blank=True)
    poster_path = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255,null=True,blank=True)
    genres = models.CharField(max_length=255,null=True,blank=True)
    production_companies = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    spoken_languages = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie',)

    def __str__(self):
        return str(self.movie.title) + ' - ' + str(self.user.username)

class WatchHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie',)
    def __str__(self):
        return str(self.movie.title) + ' - ' + str(self.user.username)

