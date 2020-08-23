from sqlite3.dbapi2 import version
from tkinter import *
from tkinter import messagebox
import sqlite3
import os

version="0.0"

# Función para mostrar información sobre la aplicación en Acerca de...
def informacion():
    messagebox.showinfo("Almacenamiento usuarios y contraseñas",
                        f"Versión: {version}\n\nCreada por IBJ como práctica para el curso de YouTube - Python, del canal 'Píldoras Informáticas'")

# Función para salir de la aplicación con ventana emergente.
def salirAplicacion():
    valor = messagebox.askokcancel("Salir de la aplicación", "Quieres salir?")
    if valor == True:
        root.destroy()

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
    pass

# Función para tomar el campo de entrada identificador y buscar un registro concreto
# o tomar el campo descripción y buscar todos los que coincidan con el patrón informado
def operRead():
    pass

# Función para tomar los cmapos de entrada y actualizar el registro que coincida con el identificador informado
def operUpdate():
    pass

# Función para eliminar el registro que coincida con el identificador informado
def operDelete():
    pass


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Comprobamos si la bbdd local de aplicación existe y si no es así, la creamos.
try:
    file=open('cred_crud.db','r')
    file.close()
    print("La bbdd ya existía. No es necesario crearla.")
except:
    conexion_bbdd = sqlite3.connect("cred_crud.db")
    #cursor_bbdd = conexion_bbdd.cursor()
    #cursor_bbdd.close()
    conexion_bbdd.close()
    print("La bbdd no existía y se ha creado.")

# Creamos la ventana principal, con el menú.
root = Tk()
root.title("Almacenamiento usuarios y contraseñas")

# Creamos elemento menú principal
barraMenu = Menu(root)
root.config(menu=barraMenu)

# Creamos opción Aplicación de manú principal y sus opciones
opcion1Menu = Menu(barraMenu, tearoff=False)
barraMenu.add_cascade(label="Aplicación", menu=opcion1Menu)
opcion1Menu.add_cascade(label="Eliminar memoria local")
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


root.mainloop()
