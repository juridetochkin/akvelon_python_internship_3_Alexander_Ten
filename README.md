<h1>Financial manager REST API. </h1>
<p> In Development... </p>

<h3>Host on:</h3>
http://206.189.100.117:8000/

<h3>Swagger:</h3>
https://app.swaggerhub.com/apis/juridetochkin/financial_manager_api/v1

<h3>To run tests:</h3>
run /manage.py test<br>
(Make sure your Postgres admin has a permission to create new Database!<br>
  Django will create a temporary db for testing.)


<h2>To deploy:</h2>
<h3>The project is deployed with the following requirements:</h3>
<p>Ubuntu 20.04<br>
PostgreSQL 13.2<br>
nginx 1.18.0<br>
Python 3.8<br>
... for Python requirements follow requirements.txt<br>

Install Python 3.8, pip, and python virtualenv<br>
Install Nginx 1.18.0<br>
Install PostgreSQL and create a new DB.<br>
Make sure that the DB admin has a permissions to create new databases,<br>
it's needed for Django to create a test DB if you need to use unittests.<br>

'git clone' the repo.<br>

pip install -r requirements.txt in your activated virtualenv<br>

To store and pass Postgres and Django secret variables to settings.py,<br>
python dotenv package is used in this project. It's already installed with the previous step,<br>
so create a .env file in the projects directory and fill it with variables you need,<br>
then configure settings.py.<br>

Run /manage.py migrate<br>

Configure: <br>
- fin.uwsgi.ini
- nginx.conf
- uwsgi_params<br>
    with parameters and paths you need
  
Create a symlink for Nginx to get your nginx.conf :<br>
sudo ln -s /full/path/to/your/nginx.conf /etc/nginx/sites-enabled/

Start Nginx<br>

Strart uWSGI:<br>
uwsgi --ini /fin_uwsgi.ini


Congrats!<br>
If you have any questions feel free to email