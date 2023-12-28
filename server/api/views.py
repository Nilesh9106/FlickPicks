from .funs import *
from django.db.models import Q
from datetime import date
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


@api_view(['GET'])
@permission_classes([AllowAny])
def allMovies(request):
    q = request.query_params.get("q")
    if q is not None:
        movies = Movie.objects.filter(Q(title__icontains=q) | Q(keywords__icontains=q))
        serializers = MovieSerializer(movies,many=True)
        return Response({'status':"success","movies":serializers.data},status=status.HTTP_200_OK)
    
    latest = Movie.objects.filter(status='Released').order_by('-release_date')[:20]
    action = Movie.objects.filter(status='Released',genres__icontains='Action').order_by('-popularity')[:20]
    bio = Movie.objects.filter(Q(keywords__icontains='biography') | Q(keywords__icontains='biopic')).order_by('-popularity')[:20]
    serializers = MovieSerializer(latest, many=True)  
    latest = serializers.data
    serializers = MovieSerializer(action, many=True)
    action = serializers.data
    serializers = MovieSerializer(bio,many=True)
    bio = serializers.data
    return Response({'status': 'success', "latest":latest,"action":action,"bio":bio}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendMovies(request):
    movies = watch_recommend(request.user)
    return Response({"status":"success","movies":movies},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorites(request):
    movies = Favorite.objects.filter(user=request.user)
    serializers = FavoriteSerializer(movies,many=True)
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
    serializers = MovieSerializer(movie)
    return Response({"status":"success","movie":serializers.data},status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_view(request):
    histories = WatchHistory.objects.filter(user=request.user).order_by('-added')
    print(histories)
    serializers = WatchHistorySerializer(histories,many=True)
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






