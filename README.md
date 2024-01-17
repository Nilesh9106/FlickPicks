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

3. create .env file in server directory and add the following lines to it
```env
POSTGRES_URL=<postgres url>
PGNAME=
PGUSER=
POSTGRES_PASSWORD=
PGHOST=
PGPORT=
```
4. create a postgres database and add the database name, username, password, host, and port to the .env file
5. run the following command to create the database tables
```bash
python manage.py migrate
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
VITE_TMDB_KEY=your_tmdb_key
```
3. run the following command to start the frontend server
```bash
yarn dev
```
