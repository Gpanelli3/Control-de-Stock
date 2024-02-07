import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass

app = Wsgiclass()



@app.ruta("/home")
def home(request, response):
    response.text = app.template(
    "home.html", context={"title": "Pagina Princip", "user": "Genaro"})

@app.ruta("/proveedores")
def otra(request, response):
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor2=conexion.cursor()
    cursor2.execute("select id_proveedor,empresa,direccion,telefono from proveedores")
    
    proveedores=[]
    for i in cursor2:
        proveedores.append(i)
    conexion.close()

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
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    cursor.execute("select cliente_id, nombre,dni,telefono from cliente")
    clientes=[]
    for i in cursor:
        clientes.append(i)
    conexion.close()


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
    cont=len(productos)
    print(cont)



    conexion2= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor2=conexion2.cursor()
    cursor2.execute("select * from categoria")

    categorias=[]
    for i in cursor2:
        categorias.append(i)
    conexion2.close()


    conexion3=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor3=conexion3.cursor()
    cursor3.execute("select id_proveedor,empresa from proveedores")

    provee=[]
    for i in cursor3:
        provee.append(i)
    conexion3.close()

    response.text = app.template(
        "productos.html",context={"title": "Productos en stock","user": cont,"producto":productos, "categoria": categorias, "proveedor": provee})



@app.ruta("/agregarProducto")
def agregarProductos(request,response):

    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
        

    id=request.POST.get('id')
    nombre=request.POST.get('nombre')
    proveedor=request.POST.get('proveedor')
    cat=request.POST.get('categoria')
    cantidad=request.POST.get('cantidad')
    costo=request.POST.get('costo')
    precio_venta=request.POST.get('venta')

    sql="INSERT INTO stock (id_producto, nombre,id_proveedor,categoria,cantidad,precio_costo,precio_venta) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    datos_producto=(id,nombre,proveedor,cat,cantidad,costo,precio_venta)
    
    cursor.execute(sql,datos_producto)
    conexion.commit()
    conexion.close()

    response.text= app.template(
        "agregarProducto.html", context={"title":"PRODUCTO AGREGADO", "user": "!"})

    



    
@app.ruta("/borrarProducto")
def borrarProducto(request,response):
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    
    id=request.POST.get('id')
    #nombre=request.POST.get('nombre')

    datId=(id,)
    #datCl=(nombre,)

    sql="delete from stock where id_producto = %s"
    datos=(datId)

    cursor.execute(sql,datos)
    conexion.commit()
    conexion.close()

    response.text=app.template(
        "borrarProducto.html",context={"title":"Borrar Producto"})
    
@app.ruta("/modificar")
def modificar(request,response):
    conexion=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    

    id=request.POST.get('id')
    costo=request.POST.get('costo')

    

    sql="update stock set precio_costo=%s where id_producto =%s"
    datos=(costo,id)

    cursor.execute(sql,datos)
    conexion.commit()
    conexion.close()

    #problemas con el precio venta
    conexion2=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor2=conexion.cursor()
    
    id2=request.POST.get('id')
    venta=request.POST.get('venta')

    sql2="update stock set precio_venta=%s where id_producto=%s"

    data=(venta,id2)
    cursor2.execute(sql2,data)
    conexion.commit()
    conexion.close()
    
    response.text=app.template(
        "modificar.html",context={"title":"modificar Producto", "user": "modificar Producto"})




@app.ruta("/facturas")
def facturas(request,response):
    conexion=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    sql="SELECT factura.nro_factura, cliente.nombre, factura.fecha, factura.descripcion, factura.medio_de_pago, factura.total FROM factura inner join cliente on cliente.cliente_id = id_cliente"
    cursor.execute(sql)
    fact = []
    for i in cursor:
        fact.append(i)
    #print(fact)
    conexion.close()

    response.text=app.template(
        "facturas.html",context={"user": "Facturas", "factura": fact})
        


    

    
    

@app.ruta("/ventas")
def ventas(request,response):


    # Conectar a la base de datos por segunda vez
    conexion_2=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor_2=conexion_2.cursor()

    # Obtener datos del formulario
    factura_id=request.POST.get('factura')
    cliente=request.POST.get('idcli')
    fecha=request.POST.get('fecha')
    descripcion=request.POST.get('descripcion')
    pago=request.POST.get('pago')
    descuento=request.POST.get('descuento')
    total=request.POST.get('total')

    if not descuento:
        descuento=0

    sql_2="INSERT INTO factura (nro_factura,id_cliente,fecha,descripcion,medio_de_pago,descuento,total) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    datos=(factura_id, cliente,fecha,descripcion,pago,descuento,total)

    try:
        cursor_2.execute(sql_2,datos)
        conexion_2.commit()
        print("insercion exitosa")
    except mysql.connector.Error as error:
        print("error al insertar en la base de datos", error)
    finally:
        conexion_2.close()


    response.text=app.template(
        "ventas.html",context={"user": "venta exitosamente cargada"})