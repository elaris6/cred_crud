from sqlite3.dbapi2 import IntegrityError, version
from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import random
from encryption import encrypt, decrypt

version="1.0"

# Función que se encarga de crear la BBDD local al arrancar la aplicación si esta no existe.
# También usada junto con el parámetro resteo, para regenerar la BBDD a petición del usuario.
def crearAlmacenamientoLocal(reseteo):
    try:
        file = open('cred_crud.strg', 'r')
        file.close()
    except:
        conexion_bbdd = sqlite3.connect("cred_crud.strg")
        cursor_bbdd = conexion_bbdd.cursor()
        cursor_bbdd.execute('''--sql
        CREATE TABLE CREDENCIALES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DESCRIPCION VARCHAR(60) UNIQUE,
        USUARIO VARCHAR(30),
        PASSWORD VARCHAR (200),
        COMENTARIOS VARCHAR(200))  
        --endsql''')
        cursor_bbdd.close()
        conexion_bbdd.close()
        if reseteo == True:
            messagebox.showinfo(
                "Información", "Se ha inicializado un nuevo fichero de almacenamiento.")
        else:
            messagebox.showinfo("Información", "El fichero de almacenamiento local no se ha hallado.\nSe ha inicializado un nuevo fichero de almacenamiento.")

# Función para crear registros de prueba con identificadores aleatorios del 0 al 100
def poblarBBDD():
    insert_error = 10
    for i in range(10):
        aleatNum = random.randint(0, 100)
        try:
            encryptedPassword = encrypt(bytes(f"Contraseña{aleatNum}", encoding='utf-8'), passLocal)
            cursor_bbdd.execute('''--sql
                    INSERT INTO CREDENCIALES VALUES (NULL,?,?,?,?)
                    --endsql''', (f"Entorno{aleatNum}",
                                f"Usuario{aleatNum}",
                                encryptedPassword,
                                f"Esto es un registro de prueba {aleatNum}"))
        except:
            insert_error-=1

    if insert_error < 10:
            messagebox.showerror("Información", f"Ha ocurrido un error interno.\n\nNo se han creado todos los registros de prueba.\n\nRegistros de prueba creados {insert_error}.")
    else:
        messagebox.showinfo("Registros de prueba", "Creación de registros de prueba realizada con éxito.")
            

# Función para mostrar información sobre la aplicación en Acerca de...
def informacion():
    messagebox.showinfo("Almacenamiento usuarios y contraseñas",
                        f"Versión: {version}\n\nCreada por IBJ como práctica para el curso de YouTube - Python, del canal 'Píldoras Informáticas'")

# Función para mostrar información sobre la manera de realizar las búsquedas
def informacionBusqueda():
    messagebox.showinfo("Uso de la búsqueda",
                        "Búsqueda por Identificador: Si conoces el identificador que deseas buscar, introdúcelo en el campo 'Identificador'\n\nBúsqueda por descripción: Si no conoces el identificador a buscar o deseas buscar todos los registros coincidentes con un patrón, introduce el patrón en el campo 'Descripción'")

# Función para salir de la aplicación con ventana emergente.
def salirAplicacion():
    valor = messagebox.askokcancel("Salir de la aplicación", "Quieres salir?")
    if valor == True:
        cursor_bbdd.close()
        conexion_bbdd.close()
        checkVentanaResultados()
        root.destroy()

# Función para eliniar el fichero de almacenamiento local y volver a generarlo de manera automática.
def eliminarAlacenamientoLocal():
    valor = messagebox.askokcancel("Eliminar alacenamiento", "Estás seguro de que deseas eliminar el almacenamiento local?")
    if valor == True:
        valor = messagebox.askyesno("Eliminar almacenamiento", "Seguro de verdad?\nNo hay marcha atrás, eh?")
        if valor == True:
            os.remove("cred_crud.strg")
            crearAlmacenamientoLocal(True)

# Función para borrar los campos de entrada
def cleanEntries():
    global passVisible
    identificador.set("")
    descripcion.set("")
    usuario.set("")
    password.set("")
    textComentarios.delete(1.0,END)
    passVisible = 1
    showPassword()

# Función para mostrar la password del Entry, quitando los asteriscos
def showPassword():
    global passVisible
    if passVisible == 0:
        entryPassword.config(show="")
        passVisible = 1
    else:
        entryPassword.config(show="*")
        passVisible = 0

# Función para generar una nueva ventana con los resultados de consulta
# si los resultados son más de uno
def ventanaTablaResultados(listaResultados):
    # Importamos la ventana de multiresultados
    global ventanaResultados

    # Definimos el número de filas y de columnas de la lista de resultados
    totalFilas = len(listaResultados)+1
    totalColumnas = len(listaResultados[0])
    encabezados = ['IDENTIFICADOR', 'DESCRIPCION','USUARIO', 'CONTRASEÑA', 'COMENTARIOS']

    # Creamos nueva ventana para resultados múltiples si no existe, y si existe la restruimos y regeneramos
    try:
        if ventanaResultados.state() == "normal":
            ventanaResultados.destroy()
            ventanaResultados = Tk()
    except:
        ventanaResultados = Tk()
    finally:
        ventanaResultados.title(f"Resultados de búsqueda: {len(listaResultados)}")

    #Creamos tabla de campos Entry y poblamos con la lista de resultados
    for i in range(totalFilas):
        for j in range(totalColumnas):
            e = Entry(ventanaResultados,width=15,justify="center")
            if j == totalColumnas-1:
                e.config(width=40)
            elif j == totalColumnas-2 and i != 0:
                e.config(show='*')
            e.grid(row=i,column=j)
            if i == 0:
                e.insert(END,encabezados[j])
                e.config(bg="black",fg="white")
            else:
                e.insert(END,listaResultados[i-1][j])

    ventanaResultados.mainloop()

# Función para comprobar si existe alguna ventana abierta de resultados múltiples y en tal caso, la cierra.
def checkVentanaResultados():
    try:
        if ventanaResultados.state() == "normal":
            ventanaResultados.destroy()
    except:
        return 0
    
# Función para tomar los campos de entrada e insertarlos como un nuevo registro almacenado
def operCreate():
    # Comprobamos si hay alguna ventana de resultados abierta y la cerramos
    checkVentanaResultados()

    global passLocal
    if entryDescripcion.get()=="" or entryUsuario.get() =="" or entryPassword.get() =="":
        messagebox.showerror("Información", "Alguno de los campos obligatorios está vacío.\n\nPor favor, rellene campos Descripción, Usuario y Contraseña")
        pass
    else:
        try:
            encryptedPassword = encrypt(
                bytes(entryPassword.get(), encoding='utf-8'), passLocal)
            cursor_bbdd.execute('''--sql
                INSERT INTO CREDENCIALES VALUES (NULL,?,?,?,?)
                --endsql''',(entryDescripcion.get(), entryUsuario.get(), encryptedPassword, textComentarios.get("1.0", END)))
            messagebox.showinfo("Información","Nuevo registro insertado!")
            cleanEntries()
        except IntegrityError:
            messagebox.showerror("Registro duplicado", "Ya existe un registro con la misma descripción.\n\nPor favor, introduce una descrpción única.")

# Función para tomar el campo de entrada identificador y buscar un registro concreto
# o tomar el campo descripción y buscar todos los que coincidan con el patrón informado
def operRead():
    global passLocal

    # Comprobamos si hay alguna ventana de resultados abierta y la cerramos
    checkVentanaResultados()

    idBuscar = entryIdentificador.get()
    descBuscar = entryDescripcion.get()
    cleanEntries()
# Comentado para permitir la búsqueda completa sin filtros    
#    if idBuscar == "" and descBuscar == "":
#        messagebox.showerror(
#            "Información", "Los campos de búsqueda están vacíos.\n\nPor favor, informe algún valor en 'Identificador' o 'Descripción'.")
#        pass
    if idBuscar != "":
        cursor_bbdd.execute('''--sql
                            SELECT * FROM CREDENCIALES WHERE ID = ?
                            --endsql''', (idBuscar,))
        resultadoQuery = cursor_bbdd.fetchall()
        if len(resultadoQuery) == 0:
            identificador.set(idBuscar)
            messagebox.showerror("Información", "Ningún registro encontrado con el identificador informado.")
        else:
            identificador.set(idBuscar)
            descripcion.set(resultadoQuery[0][1])
            usuario.set(resultadoQuery[0][2])
            password.set(str(decrypt(resultadoQuery[0][3],passLocal),encoding="utf8"))
            textComentarios.delete(1.0, END)
            textComentarios.insert(1.0,resultadoQuery[0][4])
    else:
        descBuscarSQL = '%'+descBuscar+'%'
        cursor_bbdd.execute('''--sql
                    SELECT * FROM CREDENCIALES WHERE DESCRIPCION LIKE ? ORDER BY DESCRIPCION ASC
                    --endsql''', (descBuscarSQL,))
        resultadoQuery = cursor_bbdd.fetchall()
        if len(resultadoQuery) == 0:
            descripcion.set(descBuscar)
            messagebox.showerror("Información", "Ningún registro encontrado con la descripción informada.")
        elif len(resultadoQuery) == 1:
            identificador.set(resultadoQuery[0][0])
            descripcion.set(resultadoQuery[0][1])
            usuario.set(resultadoQuery[0][2])
            password.set(resultadoQuery[0][3])
            textComentarios.delete(1.0, END)
            textComentarios.insert(1.0, resultadoQuery[0][4])
        else:
            ventanaTablaResultados(resultadoQuery)

# Función para tomar los cmapos de entrada y actualizar el registro que coincida con el identificador informado
def operUpdate():
    # Comprobamos si hay alguna ventana de resultados abierta y la cerramos
    checkVentanaResultados()

    if entryDescripcion.get() == "" or entryUsuario.get() == "" or entryPassword.get() == "":
        messagebox.showerror(
            "Información", "Alguno de los campos obligatorios está vacío.\n\nPor favor, rellene campos Descripción, Usuario y Contraseña")
        pass
    else:
        idModificar = (entryIdentificador.get())
        cursor_bbdd.execute('''--sql
                            SELECT ID FROM CREDENCIALES WHERE ID = ?
                            --endsql''', (idModificar,))
        resultadoQuery = cursor_bbdd.fetchall()
        if len(resultadoQuery) == 0:
            messagebox.showerror(
                "Información", "Ningún registro encontrado con el identificador informado.")
        else:
            cursor_bbdd.execute('''--sql
                UPDATE CREDENCIALES SET DESCRIPCION=?, USUARIO=?, PASSWORD=?,COMENTARIOS=? WHERE ID = ?
                --endsql''', (entryDescripcion.get(), entryUsuario.get(), entryPassword.get(), textComentarios.get("1.0", END), idModificar,))
            messagebox.showinfo("Información", "Registro modificado!")
            cleanEntries()

# Función para eliminar el registro que coincida con el identificador informado
def operDelete():
    # Comprobamos si hay alguna ventana de resultados abierta y la cerramos
    checkVentanaResultados()

    idEliminar = (entryIdentificador.get())
    if idEliminar == "":
        messagebox.showerror(
            "Información", "El campo identificador está vacío.\n\nPor favor, informe un valor válido.")
        pass
    else:
        cursor_bbdd.execute('''--sql
                            SELECT ID FROM CREDENCIALES WHERE ID = ?
                            --endsql''',(idEliminar,))
        resultadoQuery = cursor_bbdd.fetchall()
        if len(resultadoQuery) == 0:
            messagebox.showerror(
                "Información", "Ningún registro encontrado con el identificador informado.")
        else:
            cursor_bbdd.execute('''--sql
                DELETE FROM CREDENCIALES WHERE ID=?
                --endsql''', (idEliminar,))
            conexion_bbdd.commit()
            messagebox.showinfo("Información", "Registro eliminado!")
            cleanEntries()

""" BLOQUE PRINCIPAL DEL PROGRAMA """

os.chdir(os.path.dirname(os.path.abspath(__file__)))
passVisible = 0
passLocal = bytes("Oe06UKJ$7E*wvGf9_qA&",encoding="utf8")

# Creamos la ventana principal, y título
root = Tk()
root.title("Almacenamiento usuarios y contraseñas")

# Creamos elemento menú principal
barraMenu = Menu(root)
root.config(menu=barraMenu)

# Creamos opción Aplicación de manú principal y sus opciones
opcion1Menu = Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="Aplicación", menu=opcion1Menu)
opcion1Menu.add_cascade(label="Crear registros de prueba", command=poblarBBDD)
opcion1Menu.add_cascade(label="Eliminar memoria local", command=eliminarAlacenamientoLocal)
opcion1Menu.add_separator()  # Separador entre elemenos de menú
opcion1Menu.add_command(label="Salir", command=salirAplicacion)

# Creamos opción CRUD del menú principal y sus opciones
opcion2Menu = Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="CRUD", menu=opcion2Menu)
opcion2Menu.add_command(label="Create",command=operCreate)
opcion2Menu.add_cascade(label="Read",command=operRead)
opcion2Menu.add_cascade(label="Update",command=operUpdate)
opcion2Menu.add_cascade(label="Delete",command=operDelete)
opcion2Menu.add_separator()  # Separador entre elemenos de menú
opcion2Menu.add_cascade(label="Limpiar", command=cleanEntries)

# Creamos opción Ayuda del menú principal y sus opciones
opcion3Menu = Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="Ayuda", menu=opcion3Menu)
opcion3Menu.add_command(label="Uso de búsqueda",command=informacionBusqueda)
opcion3Menu.add_command(label="Acerca de...", command=informacion)

# Creamos frame separador entre la barra de menús y el cuerpo con los campos
frameSeparador1 = Frame(root, height="10")
frameSeparador1.pack()

# Creamos frame en el que colocar todas los campos de entrada e información
frameEntry = Frame(root, width="500", height="500")
frameEntry.pack()

identificador = StringVar()
labelIdentificador = Label(frameEntry, text="Identificador:")
labelIdentificador.grid(row=0, column=0, sticky="e", pady=5, padx=5)
entryIdentificador = Entry(frameEntry, bg="lightgrey", textvariable=identificador)
entryIdentificador.grid(row=0, column=1, columnspan=4, pady=5, padx=5)
entryIdentificador.config(width=40)

descripcion = StringVar()
labelDescripcion = Label(frameEntry, text="Descripción:")
labelDescripcion.grid(row=1, column=0, sticky="e", pady=5, padx=5)
entryDescripcion = Entry(frameEntry, textvariable=descripcion)
entryDescripcion.grid(row=1, column=1, columnspan=4, pady=5, padx=5)
entryDescripcion.config(width=40)

usuario = StringVar()
labelUsuario = Label(frameEntry, text="Usuario:")
labelUsuario.grid(row=2, column=0, sticky="e", pady=5, padx=5)
entryUsuario = Entry(frameEntry, textvariable=usuario)
entryUsuario.grid(row=2, column=1, columnspan=4, pady=5, padx=5)
entryUsuario.config(width=40)

password = StringVar()
labelPassword = Label(frameEntry, text="Contraseña:")
labelPassword.grid(row=3, column=0, sticky="e", pady=5, padx=5)
entryPassword = Entry(frameEntry, textvariable=password)
entryPassword.grid(row=3, column=1, columnspan=3, pady=5, padx=5)
entryPassword.config(show="*")
entryPassword.config(width=36)
botonShowPassword = Button(frameEntry, text="Ver",command=showPassword)
botonShowPassword.grid(row=3,column=4)


labelComentarios = Label(frameEntry, text="Comentarios:")
labelComentarios.grid(row=4, column=0, sticky="e", pady=5, padx=5)
textComentarios = Text(frameEntry, width=20, height=5)
textComentarios.grid(row=4, column=1, columnspan=3, pady="5", padx="5")
scrollComentarios = Scrollbar(frameEntry, command=textComentarios.yview)
scrollComentarios.grid(row=4, column=4, sticky="nsew")
textComentarios.config(width=27, yscrollcommand=scrollComentarios.set)

# Creamos frame separador entre el cuerpo con los campos la barra inferior de botones
frameSeparador2 = Frame(root, height="20")
frameSeparador2.pack()


# Creamos frame en el que colocar los botones CRUD
frameButtons = Frame(root, width="500", height="100", bg="lightgrey")
frameButtons.pack()

# Creamos botones de acción CRUD
botonClean = Button(frameButtons, text="Limpiar", width=8, height=2, command=cleanEntries)
botonClean.grid(row=0, column=0, pady=15, padx=10)

botonCreate = Button(frameButtons, text="Create", width=8, height=2, command=operCreate)
botonCreate.grid(row=0, column=1, pady=15, padx=10)

botonRead = Button(frameButtons, text="Read", width=8, height=2, command=operRead)
botonRead.grid(row=0, column=2, pady=15, padx=10)

botonUpdate = Button(frameButtons, text="Update", width=8, height=2, command=operUpdate)
botonUpdate.grid(row=0, column=3, pady=15, padx=1)

botonDelete = Button(frameButtons, text="Delete", width=8, height=2, command=operDelete)
botonDelete.grid(row = 0, column = 4, pady = 15, padx = 10)

labelVersion = Label(frameButtons, bg="lightgrey", text=f"Version: {version}")
labelVersion.grid(row = 1, column = 4, pady = 5, padx = 5)

# Tras inicializar la interfaz, comprobamos si la bbdd local de aplicación existe y si no es así, la creamos.
crearAlmacenamientoLocal(False)

conexion_bbdd = sqlite3.connect("cred_crud.strg")
cursor_bbdd = conexion_bbdd.cursor()

# Bucle ventana principal
root.mainloop()
