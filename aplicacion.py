import mysql.connector
from jinja2 import environment
from apiwsgi import Wsgiclass



app = Wsgiclass()
@app.ruta("/")
def productos(request, response):
    #conexion para imprimir los productos
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    
    productos=[]
    cursor.execute("select id_producto,nombre,cantidad,precio_costo,precio_venta from stock order by id_producto DESC")

    for i in cursor:
        productos.append(i)
    conexion.close()
    cont=len(productos)

    response.text = app.template(
        "inicio.html",context={"title": "Productos en stock","user": cont,"producto":productos})


@app.ruta("/homeAdmin")
def productos(request, response):
    #conexion para imprimir los productos
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    
    productos=[]
    cursor.execute("select id_producto,nombre,cantidad,precio_costo,precio_venta from stock order by id_producto DESC")

    for i in cursor:
        productos.append(i)
    conexion.close()
    cont=len(productos)

    response.text = app.template(
        "productos.html",context={"title": "Productos en stock","user": cont,"producto":productos})

    




@app.ruta("/proveedores")
def proveedores(request, response):
    #imprimir los proveedores
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
    #dar de alta proveedores
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    nombre_proveedor=request.POST.get('nombre')
    direccion=request.POST.get('direccion')
    telefono=request.POST.get('telefono')

    sql="INSERT INTO proveedores (empresa,direccion,telefono) VALUES (%s,%s,%s)"

    try:
        datos_proveedor=(nombre_proveedor,direccion,telefono)

        cursor.execute(sql,datos_proveedor)
        conexion.commit()
    except mysql.connector.Error as error:
        print("error al actualizar en la base de datos", error)
    conexion.close()

    response.text=app.template(
        "altaprovee.html",context={"user": "Usuario Cargado"})


@app.ruta("/clientes")
def cliente(request,response):
    #imprimir todos los clientes
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
    #alta clientes mediante un insert
    conexion= mysql.connector.connect(host='localhost',
                                    user='genaro',
                                    passwd='password',
                                    database='stock_control')
    cursor3=conexion.cursor()

    nombre_cliente=request.POST.get('nombre')
    dni_cliente=request.POST.get('dni')
    telefono_cliente=request.POST.get('telefono')

    sql="INSERT INTO cliente (nombre,dni,telefono) VALUES (%s,%s,%s)"
    try:
        datos_cliente=(nombre_cliente,dni_cliente,telefono_cliente)
        cursor3.execute(sql,datos_cliente)
        conexion.commit()
    except mysql.connector.Error as error:
        print("error al actualizar en la base de datos", error)
    conexion.close()
    
    response.text=app.template(
        "altaclientes.html",context={"user": "Usuario Cargado"})
    


@app.ruta("/insertar")
def insertar(request,response):
    #conexion para traer los proveedores 
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

    response.text = app.template("agregarProducto.html", context={"proveedor":provee})
    

@app.ruta("/agregar")
def agregar (request,response):

    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    nombre=request.POST.get('nombre')
    proveedor=request.POST.get('proveedor')
    cat=request.POST.get('categoria')
    cantidad=request.POST.get('cantidad')
    costo=request.POST.get('costo')

    nombreLow=nombre.lower()
    precioInt=int(costo)
    venta=precioInt + 3000

    sql="INSERT INTO stock (nombre,id_proveedor,categoria,cantidad,precio_costo,precio_venta) VALUES(%s,%s,%s,%s,%s,%s)"
    


    datos_producto=(nombreLow,proveedor,cat,cantidad,costo,venta)
    cursor.execute(sql,datos_producto)
    prod=cursor.fetchone()

    conexion.commit()
    conexion.close()

    if prod:

        response.status_code = 302
        response.headers['Location'] = '/homeAdmin'

    response.text=app.template(
        "update.html")
    
@app.ruta("/borrarProductos")
def borrarProductos(request,response):
    conexion_3= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor_3=conexion_3.cursor()

    id=request.POST.get('id')
    datId=(id,)

    sql ="DELETE FROM detalle_factura WHERE id_productos = %s;"
    datos=(datId)

    cursor_3.execute(sql,datos)
    conexion_3.commit()
    conexion_3.close()

    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    
    id=request.POST.get('id')

    datId=(id,)

    sql="delete from stock where id_producto = %s"
    datos=(datId)

    cursor.execute(sql,datos)
    conexion.commit()
    conexion.close()



    #conexion para imprimir los productos
    conexion_2= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor_2=conexion_2.cursor()
    
    productos=[]
    cursor_2.execute("select id_producto,nombre,cantidad,precio_costo,precio_venta from stock order by id_producto DESC")

    for i in cursor_2:
        productos.append(i)
    conexion_2.close()

    

    ##################DELETE
    
    response.text=app.template(
        "borrarProducto.html",context={"title":"Borrar Producto", "producto":productos})


@app.ruta("/modificar")
def modificar(request,response):

    #conexion base de datos para traer todos los productos
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    productos=[]
    cursor.execute("select id_producto,nombre,cantidad,precio_costo,precio_venta from stock")

    for i in cursor:
        productos.append(i)
    conexion.close()
    
    response.text=app.template(
        "modificar.html",context={"producto":productos})



@app.ruta("/updateProductos")
def updateProductos(request,response):

    #conexion base de datos para update de costo
    conexion2=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor2=conexion2.cursor()
    

    nombre=request.POST.get('id')
    costo=request.POST.get('costo')

    costInt=int(costo)
    venta=(costInt*1.30)

    sql="update stock set precio_costo=%s, precio_venta=%s where nombre =%s"
    
    try:
        datos=(costo,venta, nombre)

        cursor2.execute(sql,datos)

        conexion2.commit()
        
        print("actualizacion correcta")
        #print(venta)

    except mysql.connector.Error as error:
        print("error al actualizar en la base de datos", error)

        conexion2.close()
    response.text=app.template(
        "update.html", context={"mensage":"actualizacion correcta"})




@app.ruta("/facturas")
def facturas(request,response):
    conexion=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()
    	
    sql="SELECT factura.nro_factura, cliente.nombre, factura.fecha, factura.descripcion, factura.medio_de_pago, factura.total FROM factura inner join cliente on cliente.cliente_id = id_cliente order by nro_factura"
    try:
        cursor.execute(sql)
        facturas = []
        for i in cursor:
            facturas.append(i)

        fact=[]
        for i in range(len(facturas)):
            fact.append(facturas[-i-1])

    except mysql.connector.Error as error:
        print("error al actualizar en la base de datos", error)
    conexion.close()
    response.text=app.template(
        "facturas.html",context={"user": "Facturas", "factura": fact})



@app.ruta("/bajaFactura")
def bajaFactura(request,response):
    #--conexion para borrar facturas
    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor=conexion.cursor()

    fact=request.POST.get('id')

    sql ="DELETE FROM detalle_factura WHERE factura_idfactura = %s;"

    datId=(fact,)
    cursor.execute(sql,datId)
    conexion.commit()
    conexion.close()

    ##############__----------------------------
    conexionDos= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursorDos=conexionDos.cursor()

    fact=request.POST.get('id')

    sqlDos="delete from factura where nro_factura = %s"
    data=(fact,)

    cursorDos.execute(sqlDos,data)
    
    conexionDos.commit()
    conexionDos.close()


    ######################################

    conexionTres= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursorTres=conexionTres.cursor()
    
    sql="SELECT factura.nro_factura, cliente.nombre, factura.fecha, factura.descripcion, factura.medio_de_pago, factura.total FROM factura inner join cliente on cliente.cliente_id = id_cliente order by nro_factura"
    
    cursorTres.execute(sql)
    facturas = []
    for i in cursorTres:
        facturas.append(i)

    fact=[]
    for i in range(len(facturas)):
        fact.append(facturas[-i-1])


    response.text=app.template(
        "bajaFacturas.html", context={"factura": fact})    


        


@app.ruta("/ventas")
def ventas(request,response):


    # Conectar a la base de datos
    conexion_2=mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    cursor_2=conexion_2.cursor()

    # Obtener datos del formulario

    cliente=request.POST.get('idcli')
    fecha=request.POST.get('fecha')
    descripcion=request.POST.get('descripcion')
    pago=request.POST.get('pago')
    descuento=request.POST.get('descuento')
    total=request.POST.get('total')

    if not descuento:
        descuento=0

    sql_2="INSERT INTO factura (id_cliente,fecha,descripcion,medio_de_pago,descuento,total) VALUES (%s,%s,%s,%s,%s,%s)"
    datos=( cliente,fecha,descripcion,pago,descuento,total)

    try:
        cursor_2.execute(sql_2,datos)
        conexion_2.commit()
        print("insercion exitosa")


    except mysql.connector.Error as error:
        print("error al insertar en la base de datos", error)

    conexion_2.close()
    response.text=app.template(
        "ventas.html",context={"user": "venta exitosamente cargada"})







@app.ruta("/login")
def login(request,response):
    email=request.POST.get('email')
    password=request.POST.get('password')

    conexion= mysql.connector.connect(host='localhost',
                                  user='genaro',
                                  passwd='password',
                                  database='stock_control')
    
    cursor=conexion.cursor()

    cursor.execute("SELECT email, password FROM usuarios WHERE email = %s", (email,))
    user=cursor.fetchone()
    conexion.close()
    
    if user:
        response.status_code = 302
        response.headers['Location'] = '/homeAdmin'
        print("usuario encontrado")
    else:
        response.status_code = 404
        response.headers['Location'] = '/login'

        print("no encontrado")

    response.text=app.template(
        "ingreso.html")
    
@app.ruta("/logout")
def logout(request,response):
    response.status_code = 302
    response.headers['Location'] = '/login'

