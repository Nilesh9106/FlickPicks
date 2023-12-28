# FlickPicks- Movie recommendation System

## To setup backend api for this project follow below steps
1. go to server directory and in that directory run following command to create virtual environment
```bash
cd server
virtualenv env
```
**Note**: if you don't have virtualenv installed then install it using below command
```bash
pip install virtualenv
```
2. install all required packages using below command
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
7. Run following command to add all movies from csv file to database
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

## To setup frontend for this project follow below steps
1. go to flickpicks directory and in that directory run following command to install all required packages
```bash
cd flickpicks
yarn install
```
2. create .env file in flickpicks directory and add following line to it
```bash
VITE_API_URI=http://127.0.0.1:8000/api/
```
3. run following command to start the frontend server
```bash
yarn dev
```
