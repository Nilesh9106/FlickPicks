from rest_framework import serializers
from .models import *

class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields =  '__all__'

class MovieSerializer(serializers.ModelSerializer):
    isFavorite = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = '__all__'
    def get_isFavorite(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            user = request.user
        return Favorite.objects.filter(movie=obj, user=user).exists()

class FavoriteSerializer(serializers.ModelSerializer):
    user = userSerializers()
    movie = serializers.SerializerMethodField()
    class Meta:
        model = Favorite
        fields = '__all__'
    
    def get_movie(self, obj):
        serializers = MovieSerializer(obj.movie,context={"request":self.context.get("request")})
        return serializers.data

class WatchHistorySerializer(serializers.ModelSerializer):
    user = userSerializers()
    movie = serializers.SerializerMethodField()
    class Meta:
        model = WatchHistory
        fields = '__all__'

    def get_movie(self, obj):
        serializers = MovieSerializer(obj.movie,context={"request":self.context.get("request")})
        return serializers.data

