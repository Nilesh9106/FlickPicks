from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import *
from .serializers import *

class AllMoviesTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_all_movies_without_query_param(self):
        url = reverse('allMovies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('latest', response.data)
        self.assertIn('action', response.data)
        self.assertIn('bio', response.data)

    def test_all_movies_with_query_param(self):
        url = reverse('allMovies')
        response = self.client.get(url, {'q': 'action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertNotIn('latest', response.data)
        self.assertNotIn('action', response.data)
        self.assertNotIn('bio', response.data)
    
class MovieViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(title="test",vote_average=7.5,status="Released",release_date="2021-01-01",revenue=1000000,runtime=120,credit="Tom",budget=1000000,overview="test",popularity=7.5,poster_path="test",tagline="test",genres="test",production_companies="test",keywords="test",spoken_languages="test")
        self.movie = Movie.objects.get(title="test")
        self.movie_id = self.movie.id

    def test_movie_view_with_authenticated_user(self):
        # Create an authenticated user
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=user)

        # Make a GET request to the movieView endpoint
        response = self.client.get(reverse("movieApi", args=[self.movie_id]))

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the movie details are returned in the response
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["movie"], MovieSerializer(self.movie).data)

        # Assert that the recommendations and productions are returned in the response
        self.assertEqual(len(response.data["recommendations"]), 0)
        self.assertEqual(len(response.data["productions"]), 1)

    def test_movie_view_with_unauthenticated_user(self):
        # Make a GET request to the movieView endpoint
        response = self.client.get(reverse("movieApi", args=[self.movie_id]))

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the movie details are returned in the response
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["movie"], MovieSerializer(self.movie).data)

        # Assert that the recommendations and productions are returned in the response
        self.assertEqual(len(response.data["recommendations"]), 0)
        self.assertEqual(len(response.data["productions"]), 1)

    def test_movie_view_with_invalid_movie_id(self):
        # Make a GET request to the movieView endpoint with an invalid movie ID
        response = self.client.get(reverse("movieApi", args=[999]))

        # Assert that the response status code is 404 Not Found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(response.data["message"], "movie not found")


class RemoveFromFavTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Movie.objects.create(title='Test Movie')
        self.movie = Movie.objects.get(title="Test Movie")
        self.favorite = Favorite.objects.create(user=self.user, movie=self.movie)

    def test_remove_from_fav_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('removeFromFavApi'), {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'success', 'message': 'movie removed from favorites'})
        self.assertFalse(Favorite.objects.filter(user=self.user, movie=self.movie).exists())

    def test_remove_from_fav_missing_movie_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('removeFromFavApi'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'failed', 'message': 'movie_id is required'})

    def test_remove_from_fav_movie_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('removeFromFavApi'), {'movie_id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'status': 'failed', 'message': 'movie not found'})

    def test_remove_from_fav_movie_not_in_favorites(self):
        self.client.force_authenticate(user=self.user)
        self.favorite.delete()
        response = self.client.post(reverse('removeFromFavApi'), {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'status': 'failed', 'message': 'movie not in favorites'})

class AddToFavTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Movie.objects.create(title='Test Movie')
        self.movie = Movie.objects.get(title="Test Movie")

    def test_add_to_fav_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('addToFavApi'), {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'movie added to favorites')

    def test_add_to_fav_missing_movie_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('addToFavApi'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'movie_id is required')

    def test_add_to_fav_movie_not_found(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('addToFavApi'), {'movie_id': 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'movie not found')

    def test_add_to_fav_already_in_favorites(self):
        Favorite.objects.create(user=self.user, movie=self.movie)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('addToFavApi'), {'movie_id': self.movie.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'movie already in favorites')

class FavoritesViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        Movie.objects.create(title='Test Movie')
        Movie.objects.create(title='Test Movie 2')
        self.movie1 = Movie.objects.get(title="Test Movie")
        self.movie2 = Movie.objects.get(title="Test Movie 2")

    def test_favorites_list(self):
        # Create some favorite movies for the user
        Favorite.objects.create(user=self.user, movie=self.movie1)
        Favorite.objects.create(user=self.user, movie=self.movie2)

        # Make a GET request to the favorites endpoint
        url = reverse('favoritesApi')
        response = self.client.get(url)

        # Check that the response has a status code of 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains the correct data
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('movies', response.data)

class SignupTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        data = {
            'username': 'exist',
            'email': 'exist@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/register', data)

    def test_signup_success(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('token', response.data)
        self.assertIn('userInfo', response.data)
        self.assertEqual(response.data['message'], 'Signup successful')

    def test_signup_missing_fields(self):
        data = {
            'username': 'testuser',
            'email': '',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/register', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'All username, email and password are required')

    def test_signup_existing_user(self):
        data = {
            'username': 'exist',
            'email': 'exist@example.com',
            'password': 'testpassword'
        }
        response = self.client.post('/api/user/register', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'failed')
        self.assertEqual(response.data['message'], 'User with this username or email already exists')

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('loginApi')

    def test_login_success(self):
        # Create a test user
        user = User.objects.create_user(username='testuser',email="test@gmail.com", password='testpassword')

        # Send a POST request to the login endpoint
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'})

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected keys
        self.assertIn('status', response.data)
        self.assertIn('token', response.data)
        self.assertIn('userInfo', response.data)
        self.assertIn('message', response.data)

        # Assert that the user's password is not included in the response
        self.assertNotIn('password', response.data['userInfo'])

    def test_login_missing_credentials(self):
        # Send a POST request to the login endpoint without providing username and password
        response = self.client.post(self.login_url, {})

        # Assert that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the response contains the expected keys
        self.assertIn('status', response.data)
        self.assertIn('message', response.data)

    def test_login_invalid_credentials(self):
        # Send a POST request to the login endpoint with invalid username and password
        response = self.client.post(self.login_url, {'username': 'invaliduser', 'password': 'invalidpassword'})

        # Assert that the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assert that the response contains the expected keys
        self.assertIn('status', response.data)
        self.assertIn('message', response.data)

class HistoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('historyApi')

    def test_clear_history(self):
        # Create a test watch history

        movie1 = Movie(title="test",vote_average=7.5,status="Released",release_date="2021-01-01",revenue=1000000,runtime=120,credit="Tom",budget=1000000,overview="test",popularity=7.5,poster_path="test",tagline="test",genres="test",production_companies="test",keywords="test",spoken_languages="test")  
        movie1.save()  

        WatchHistory.objects.create(user=self.user,movie=Movie.objects.all().first())

        # Send a GET request to the clearHistory endpoint
        response = self.client.get('/api/user/clearHistory')

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected keys
        self.assertIn('status', response.data)
        self.assertIn('message', response.data)

        # Assert that the watch history has been cleared
        self.assertEqual(WatchHistory.objects.filter(user=self.user).count(), 0)
    
    def test_history_view_with_authenticated_user(self):
        # Create some watch history objects for the user
        movie1 = Movie(title="test",vote_average=7.5,status="Released",release_date="2021-01-01",revenue=1000000,runtime=120,credit="Tom",budget=1000000,overview="test",popularity=7.5,poster_path="test",tagline="test",genres="test",production_companies="test",keywords="test",spoken_languages="test")  
        movie1.save()  
        WatchHistory.objects.create(user=self.user, movie=Movie.objects.filter(title="test").first())

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(len(response.data['histories']), 1)

    def test_history_view_with_unauthenticated_user(self):
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)