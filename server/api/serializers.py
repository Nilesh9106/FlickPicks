from rest_framework import serializers
from .models import *

class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields =  '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    user = userSerializers()
    movie = MovieSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'

class WatchHistorySerializer(serializers.ModelSerializer):
    user = userSerializers()
    movie = MovieSerializer()
    class Meta:
        model = WatchHistory
        fields = '__all__'

