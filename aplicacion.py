import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass

app = Wsgiclass()

#----------------------------------------------------CLIENTES
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor2=conexion.cursor()
clientes=[]
cursor2.execute("select cliente_id, nombre,dni,telefono from cliente")

for i in cursor2:
    clientes.append(i)
#print(clientes)

conexion.close()
#----------------------------------------------------CLIENTES
#----------------------------------------------------PROVEEDORES
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor=conexion.cursor()
cursor.execute("select id_proveedor,empresa,direccion,telefono from proveedores")

proveedores=[]
for i in cursor:
    proveedores.append(i)
conexion.close()
#----------------------------------------------------PROVEEDORES

#----------------------------------------------------PRODUCTOS
conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
cursor3=conexion.cursor()
productos=[]
cursor3.execute("select id_producto,nombre,cantidad,precio_costo,precio_venta from stock")

for i in cursor3:
    productos.append(i)
conexion.close()
#----------------------------------------------------PRODUCTOS



@app.ruta("/home")
def home(request, response):
    response.text = app.template(
    "home.html", context={"title": "Pagina Princip", "user": "Genaro"})

@app.ruta("/proveedores")
def otra(request, response):

    response.text = app.template(
    "proveedores.html", context={"title": "Pagina secundaria", "user": "Lista de Proveedores","proveedor":proveedores})


@app.ruta("/altaprovee")
def altaprovee (request,response):
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    nombre_proveedor=request.POST.get('nombre')
    direccion=request.POST.get('direccion')
    telefono=request.POST.get('telefono')

    sql="INSERT INTO proveedores (empresa,direccion,telefono) VALUES (%s,%s,%s)"
    datos_proveedor=(nombre_proveedor,direccion,telefono)

    cursor.execute(sql,datos_proveedor)
    conexion.commit()
    conexion.close()

    response.text=app.template(
        "altaprovee.html",context={"user": "Usuario Cargado"})


@app.ruta("/bajaprovee")
def bajaprovee(request,response):

    conexion= mysql.connector.connect(host='localhost',
                                    user='genaro',
                                    passwd='password',
                                    database='stock_control')
    cursor4=conexion.cursor()

    id=request.POST.get('id')
    dato_client=(id,)

    sql="delete from proveedores where id_proveedor = %s"
    datos=(dato_client)
    cursor4.execute(sql,datos)
    conexion.commit()
    conexion.close()
    
    response.text = app.template(
    "bajaprovee.html", context={"title": "Baja proveedores", "user": "Genaro"})

@app.ruta("/clientes")
def cliente(request,response):

    response.text = app.template(
    "clientes.html", context={"title": "Clientes", "user": "Lista de clientes","cliente": clientes})




@app.ruta("/altaclientes")
def altaclientes(request, response):

    conexion= mysql.connector.connect(host='localhost',
                                    user='genaro',
                                    passwd='password',
                                    database='stock_control')
    cursor3=conexion.cursor()

    nombre_cliente=request.POST.get('nombre')
    dni_cliente=request.POST.get('dni')
    telefono_cliente=request.POST.get('telefono')

    sql="INSERT INTO cliente (nombre,dni,telefono) VALUES (%s,%s,%s)"

    datos_cliente=(nombre_cliente,dni_cliente,telefono_cliente)
    cursor3.execute(sql,datos_cliente)
    conexion.commit()
    conexion.close()
    
    response.text=app.template(
        "altaclientes.html",context={"user": "Usuario Cargado"})
    


@app.ruta("/bajaclientes")
def bajacliente(request,response):

    conexion= mysql.connector.connect(host='localhost',
                                    user='genaro',
                                    passwd='password',
                                    database='stock_control')
    cursor4=conexion.cursor()

    id=request.POST.get('id')
    dato_client=(id,)

    sql="delete from cliente where cliente_id = %s"
    datos=(dato_client)
    cursor4.execute(sql,datos)
    conexion.commit()
    conexion.close()
    
    response.text = app.template(
    "bajaclientes.html", context={"title": "Baja clientes", "user": "Genaro"})


    


@app.ruta("/productos")
def productos(request, response):

    response.text = app.template(
        "productos.html",context={"title": "Productos en stock","user": "Lista de productos","producto":productos})
    


@app.ruta("/modificar")
def modificar(request,response):
    conexion= mysql.connector.connect(host='localhost',
                                    user='genaro',
                                    passwd='password',
                                    database='stock_control')
    cursor=conexion.cursor()

    



