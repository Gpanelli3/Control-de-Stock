import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass
productos=[]

#conexion base de datos--------------------------------
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor=conexion.cursor()
cursor.execute("select * from proveedores")



proveedores=[]
for i in cursor:
    proveedores.append(i)
print(proveedores)
conexion.close()
#----------------------------------------------------------------------------
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor2=conexion.cursor()


clientes=[]
cursor2.execute("select * from cliente")

for i in cursor2:
    clientes.append(i)
print(clientes)

conexion.close()
#----------------------------------------------------------------------------



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
def clientes(request,response):
     response.text = app.template(
    "clientes.html", context={"title": "Clientes", "user": "Lista de clientes","cliente":clientes})



@app.ruta("/altaclientes")
def altaclientes(request, response):

    nombre_cliente=request.POST.get('nombre')
    dni_cliente=request.POST.get('dni')
    telefono_cliente=request.POST.get('telefono')

    sql="INSERT INTO cliente (nombre,dni,telefono) VALUES (%s,%s,%s)"

    datos_cliente=(nombre_cliente,dni_cliente,telefono_cliente)
    cursor2.execute(sql,datos_cliente)
    conexion.commit()
    conexion.close()

    response.text=app.template(
        "altaclientes.html",context={"user": "Usuario Cargado"})




@app.ruta("/productos")
def productos(request, response):
    response.text = app.template(
        "productos.html",context={"title": "Productos en stock","user": "Lista de productos"})