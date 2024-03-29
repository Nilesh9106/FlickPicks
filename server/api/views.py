from .funs import *
from datetime import date
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import *
from django.db import OperationalError
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def filterView(request):
    genres = request.data.get("genres") #list of genres
    languages = request.data.get("language") # list of languages
    status1 = request.data.get("status") # list of status of movie e.g. Released, Rumored, Post Production
    sortBy = request.data.get("sortBy") # popularity, release_date, vote_average
    ascending = bool(request.data.get("ascending")) 

    if genres is None and languages is None and status1 is None and sortBy is None:
        return Response({"status":"failed","message":"Invalid query"},status=status.HTTP_400_BAD_REQUEST)
    # filter movies according to genres, languages, status and sort them sortBy
    
    queryset = Movie.objects.all()
    if genres:
        # Use Q objects to perform OR logic on genres
        genre_filters = Q()
        for genre in genres:
            genre_filters |= Q(genres__icontains=genre)
        queryset = queryset.filter(genre_filters)

    # print(request.data)
    if languages:
        queryset = queryset.filter(spoken_languages__in=languages)

    if status1:
        queryset = queryset.filter(status__in=status1)

    order_prefix = "" if ascending else "-"
    sort_criteria = f"{order_prefix}{sortBy}"

    queryset = queryset.order_by(sort_criteria)

    # Serialize the filtered and sorted queryset
    serializers = MovieSerializer(queryset[:30], many=True,context={"request":request})
    
    
    return Response({'status':"success","movies":serializers.data},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def allMovies(request):
    q = request.query_params.get("q")
    if q is not None:
        movies = Movie.objects.filter(Q(title__icontains=q) | Q(keywords__icontains=q))
        serializers = MovieSerializer(movies,many=True,context={"request":request})
        return Response({'status':"success","movies":serializers.data},status=status.HTTP_200_OK)
    
    latest = Movie.objects.filter(status='Released').order_by('-release_date')[:20]
    action = Movie.objects.filter(status='Released',genres__icontains='Action').order_by('-popularity')[:20]
    bio = Movie.objects.filter(Q(keywords__icontains='biography') | Q(keywords__icontains='biopic')).order_by('-popularity')[:20]
    serializers = MovieSerializer(latest, many=True,context={"request":request})  
    latest = serializers.data
    serializers = MovieSerializer(action, many=True,context={"request":request})
    action = serializers.data
    serializers = MovieSerializer(bio,many=True,context={"request":request})
    bio = serializers.data
    dict1 = {'status': 'success', "latest":latest,"action":action,"bio":bio}
    if request.user.is_authenticated and WatchHistory.objects.filter(user=request.user).exists():
        import random
        recommendation = watch_recommend(request.user)
        random.shuffle(recommendation)
        dict1["recommendation"] = recommendation
    
    return Response(dict1, status=status.HTTP_200_OK)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorites(request):
    movies = Favorite.objects.filter(user=request.user)
    serializers = FavoriteSerializer(movies,many=True,context={"request":request})
    return Response({"status":"success","movies":serializers.data},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addToFav(request):
    movie_id = request.data.get('movie_id')
    if movie_id is None:
        return Response({"status":"failed","message":"movie_id is required"},status=status.HTTP_400_BAD_REQUEST)
    movie = Movie.objects.filter(id=movie_id).first()
    if movie is None:
        return Response({"status":"failed","message":"movie not found"},status=status.HTTP_404_NOT_FOUND)
    fav,created = Favorite.objects.get_or_create(user=request.user,movie=movie)
    if not created:
        return Response({"status":"failed","message":"movie already in favorites"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"status":"success","message":"movie added to favorites"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeFromFav(request):
    movie_id = request.data.get('movie_id')
    if movie_id is None:
        return Response({"status":"failed","message":"movie_id is required"},status=status.HTTP_400_BAD_REQUEST)
    movie = Movie.objects.filter(id=movie_id).first()
    if movie is None:
        return Response({"status":"failed","message":"movie not found"},status=status.HTTP_404_NOT_FOUND)
    fav = Favorite.objects.filter(user=request.user,movie=movie).first()
    if fav is None:
        return Response({"status":"failed","message":"movie not in favorites"},status=status.HTTP_400_BAD_REQUEST)
    fav.delete()
    return Response({"status":"success","message":"movie removed from favorites"},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def movieView(request,movie_id):
    movie = Movie.objects.filter(id=movie_id).first()
    if movie is None:
        return Response({"status":"failed","message":"movie not found"},status=status.HTTP_404_NOT_FOUND)
    if(request.user.is_authenticated):
        try:
            WatchHistory.objects.update_or_create(user=request.user,movie=movie,defaults={'added':date.today()})
        except OperationalError:
            pass
    data = search_similar_movies(movie_id)
    recommendations = data['recommendations']

    serializers = MovieSerializer(movie,context={"request":request})

    first = movie.production_companies.split('-')
    movies_pro =[]
    if(len(first) !=0):
        first = first[0]
        movies_pro = Movie.objects.filter(production_companies__icontains = first )
        productions_ser = MovieSerializer(movies_pro,many=True,context={"request":request})
        movies_pro = productions_ser.data
    
    return Response({"status":"success","movie":serializers.data,'recommendations':recommendations,'productions':movies_pro},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_view(request):
    histories = WatchHistory.objects.filter(user=request.user).order_by('-added')
    serializers = WatchHistorySerializer(histories,many=True,context={"request":request})
    return Response({"status":"success","histories":serializers.data},status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # Your signup logic here
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password or not email:
        return Response({"status":"failed",'message': 'All username, email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(username=username,email=email)
    if not created:
        return Response({"status":"failed",'message': 'User with this username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(password)
    user.save()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    user = userSerializers(user).data
    user.pop('password')
    return Response({"status":"success",'token':access_token,'userInfo':user,'message': 'Signup successful'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    # Your login logic here
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"status":"failed",'message': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(username=username).first()

    if user is None or not user.check_password(password):
        return Response({"status":"failed",'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    user = userSerializers(user).data
    user.pop('password')
    return Response({"status":"success",'token': access_token, 'userInfo':user,'message': 'Login successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Your logout logic here
    request.user.auth_token.delete()
    return Response({"status":"success",'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def clearHistory(request):
    WatchHistory.objects.filter(user=request.user).delete()
    return Response({"status":"success",'message': 'History cleared'}, status=status.HTTP_200_OK)

