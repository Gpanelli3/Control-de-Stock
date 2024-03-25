import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass

app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    response.text = app.template(
    "home.html", context={"title": "Pagina Princip", "user": "Genaro"})