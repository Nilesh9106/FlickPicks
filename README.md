# FlickPicks- Movie Recommendation System
This project is a movie recommendation system that suggests movies to users based on a custom recommendation algorithm. The system considers various factors such as user preferences, genre preferences, and viewing history to provide personalized movie recommendations.

## To set the backend API for this project follow the below steps
1. go to the server directory and in that directory run the following command to create a virtual environment
```bash
cd server
virtualenv env
```
**Note**: if you don't have virtualenv installed then install it using the below command
```bash
pip install virtualenv
```
2. install all required packages using the below command
```bash
pip install -r requirements.txt
```
4. run this command for making migrations
```bash
python manage.py makemigrations
```
5. run migrate command for store database changes

```bash
python manage.py migrate
```
7. Run the following command to add all movies from the CSV file to the database
```bash
python manage.py runscript addmovie
```

6. run this command to start the server
```bash
python manage.py runserver
```
### for creating admin user

```bash
python manage.py createsuperuser
```

## To setup frontend for this project follow the below steps
1. go to flickpicks directory and in that directory run the following command to install all required packages
```bash
cd flickpicks
yarn install
```
2. create .env file in flickpicks directory and add the following line to it
```bash
VITE_API_URI=http://127.0.0.1:8000/api/
```
3. run the following command to start the frontend server
```bash
yarn dev
```
