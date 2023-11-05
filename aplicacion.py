import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass

#conexion base de datos--------------------------------
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor=conexion.cursor()
cursor.execute("select * from proveedores")


proveedores=[]
clientes=[]

for i in cursor:
    proveedores.append(i)
conexion.close()
#----------------------------------------------------------------------------

conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor1=conexion.cursor()
cursor1.execute("select * from cliente")

for i in cursor1:
    clientes.append(i)
conexion.close()
#conexion base de datos--------------------------------


app = Wsgiclass()

@app.ruta("/home")
def home(request, response):
    response.text = app.template(
    "home.html", context={"title": "Pagina Princip", "user": "Genaro"})

@app.ruta("/proveedores")
def otra(request, response):
    response.text = app.template(
    "proveedores.html", context={"title": "Pagina secundaria", "user": "Lista de Proveedores","proveedor":proveedores})
        
        

@app.ruta("/clientes")
def ultima(request, response):
    response.text = app.template(
    "clientes.html", context={"title": "Clientes", "user": "Lista de clientes","cliente":clientes})
