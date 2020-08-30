from sqlite3.dbapi2 import IntegrityError, version
from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import random

version="0.0"

# Función que se encarga de crear la BBDD local al arrancar la aplicación si esta no existe.
# También usada junto con el parámetro resteo, para regenerar la BBDD a petición del usuario.
def crearAlmacenamientoLocal(reseteo):
    try:
        file = open('cred_crud.sqlite', 'r')
        file.close()
    except:
        conexion_bbdd = sqlite3.connect("cred_crud.sqlite")
        cursor_bbdd = conexion_bbdd.cursor()
        cursor_bbdd.execute('''--sql
        CREATE TABLE CREDENCIALES(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DESCRIPCION VARCHAR(60) UNIQUE,
        USUARIO VARCHAR(30),
        PASSWORD VARCHAR (30),
        COMENTARIOS VARCHAR(200))  
        --endsql''')
        cursor_bbdd.close()
        conexion_bbdd.close()
        if reseteo == True:
            messagebox.showinfo(
                "Información", "Se ha inicializado un nuevo fichero de almacenamiento.")
        else:
            messagebox.showinfo("Información", "El fichero de almacenamiento local no se ha hallado.\nSe ha inicializado un nuevo fichero de almacenamiento.")

def poblarBBDD():
    insert_error = 10
    for i in range(10):
        aleatNum = random.randint(0, 100)
        try:
            cursor_bbdd.execute('''--sql
                    INSERT INTO CREDENCIALES VALUES (NULL,?,?,?,?)
                    --endsql''', (f"Entorno{aleatNum}",
                                f"Usuario{aleatNum}",
                                f"Contraseña{aleatNum}",
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

# Función para salir de la aplicación con ventana emergente.
def salirAplicacion():
    valor = messagebox.askokcancel("Salir de la aplicación", "Quieres salir?")
    if valor == True:
        cursor_bbdd.close()
        conexion_bbdd.close()
        root.destroy()

def eliminarAlacenamientoLocal():
    valor = messagebox.askokcancel("Eliminar alacenamiento", "Estás seguro de que deseas eliminar el almacenamiento local?")
    if valor == True:
        valor = messagebox.askyesno("Eliminar almacenamiento", "Seguro de verdad?\nNo hay marcha atrás, eh?")
        if valor == True:
            os.remove("cred_crud.sqlite")
            crearAlmacenamientoLocal(True)

# Función para borrar los campos de entrada
def cleanEntries():
    identificador.set("")
    descripcion.set("")
    usuario.set("")
    password.set("")
    textComentarios.delete("1.0",END)

# Función para generar una nueva ventana con los resultados de consulta
# si los resultados son más de uno
def ventanaTablaResultados():
    ventana_resultados = Tk()
    ventana_resultados.title("Resultados de búsqueda")

    ventana_resultados.mainloop()

# Función para tomar los campos de entrada e insertarlos como un nuevo registro almacenado
def operCreate():
    if entryDescripcion.get()=="" or entryUsuario.get() =="" or entryPassword.get() =="":
        messagebox.showerror("Información", "Uno de los campos obligatorios está vacío.\n\nPor favor, rellene campos Descripción, Usuario y Contraseña")
        pass
    else:
        try:
            cursor_bbdd.execute('''--sql
                INSERT INTO CREDENCIALES VALUES (NULL,?,?,?,?)
                --endsql''',(entryDescripcion.get(), entryUsuario.get(), entryPassword.get(),textComentarios.get("1.0", END)))
            messagebox.showinfo("Información","Nuevo registro insertado!")
            cleanEntries()
        except IntegrityError:
            messagebox.showerror("Registro duplicado", "Ya existe un registro con la misma descripción.\n\nPor favor, introduce una descrpción única.")

        

# Función para tomar el campo de entrada identificador y buscar un registro concreto
# o tomar el campo descripción y buscar todos los que coincidan con el patrón informado
def operRead():
    pass

# Función para tomar los cmapos de entrada y actualizar el registro que coincida con el identificador informado
def operUpdate():
    pass

# Función para eliminar el registro que coincida con el identificador informado
def operDelete():
    idEliminar = (entryIdentificador.get())
    if idEliminar == "":
        messagebox.showerror(
            "Información", "El campo identificador está vacío.\n\nPor favor, informe el un valor.")
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

# Creamos la ventana principal, con el menú.
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
opcion3Menu.add_command(label="Acerca de...",command=informacion)

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
labelPassword = Label(frameEntry, text="Password:")
labelPassword.grid(row=3, column=0, sticky="e", pady=5, padx=5)
entryPassword = Entry(frameEntry, textvariable=password)
entryPassword.grid(row=3, column=1, columnspan=4, pady=5, padx=5)
entryPassword.config(show="*")
entryPassword.config(width=40)

labelComentarios = Label(frameEntry, text="Comentarios:")
labelComentarios.grid(row=4, column=0, sticky="e", pady=5, padx=5)
textComentarios = Text(frameEntry, width="20", height="5")
textComentarios.grid(row=4, column=1, columnspan=3, pady="5", padx="5")
scrollComentarios = Scrollbar(frameEntry, command=textComentarios.yview)
scrollComentarios.grid(row=4, column=4, sticky="nsew")
textComentarios.config(width=27, yscrollcommand=scrollComentarios.set)


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

conexion_bbdd = sqlite3.connect("cred_crud.sqlite")
cursor_bbdd = conexion_bbdd.cursor()



root.mainloop()
