from tkinter import *
from tkinter import messagebox
import sqlite3
import os

# Función para mostrar información sobre la aplicación en Acerca de...
def informacion():
    messagebox.showinfo("Almacenamiento usuarios y contraseñas",
                        "Versión: 0.0\n\nCreada por IBJ como práctica para el curso de YouTube - Python, del canal 'Píldoras Informáticas'")

# Función para salir de la aplicación con ventana emergente.
def salirAplicacion():
    valor = messagebox.askokcancel("Salir de la aplicación", "Quieres salir?")
    if valor == True:
        root.destroy()

# Función para generar una nueva ventana con los resultados de consulta
# si los resultados son más de uno
def ventanaTablaResultados():
    ventana_resultados = Tk()
    ventana_resultados.title("Resultados de búsqueda")

    ventana_resultados.mainloop()

def boton():
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
opcion1Menu = Menu(barraMenu, tearoff=0)
barraMenu.add_cascade(label="Aplicación", menu=opcion1Menu)
opcion1Menu.add_cascade(label="Eliminar memoria local")
opcion1Menu.add_separator()  # Separador entre elemenos de menú
opcion1Menu.add_command(label="Salir", command=salirAplicacion)

# Creamos opción CRUD del menú principal y sus opciones
opcion2Menu = Menu(barraMenu, tearoff=0)
barraMenu.add_cascade(label="CRUD", menu=opcion2Menu)
opcion2Menu.add_command(label="Create")
opcion2Menu.add_cascade(label="Read",command=ventanaTablaResultados)
opcion2Menu.add_cascade(label="Update")
opcion2Menu.add_cascade(label="Delete")

# Creamos opción Ayuda del menú principal y sus opciones
opcion4Menu = Menu(barraMenu, tearoff=0)
barraMenu.add_cascade(label="Ayuda", menu=opcion4Menu)
opcion4Menu.add_command(label="Acerca de...",command=informacion)

# Creamos frame en el que colocar todas los campos de entrada e información
frameEntry = Frame(root, width="500", height="500", bg="lightgrey")
frameEntry.pack()

identificador = StringVar()
labelIdentificador = Label(frameEntry, text="Descripción:")
labelIdentificador.grid(row="0", column="0", sticky="e", pady=5, padx=5)
entryIdentificador = Entry(frameEntry, bg="lightgrey", textvariable=identificador)
entryIdentificador.grid(row="0", column="1", pady=5, padx=5)

descripcion = StringVar()
labelDescripcion = Label(frameEntry, text="Descripción:")
labelDescripcion.grid(row="1", column="0", sticky="e", pady=5, padx=5)
entryDescripcion = Entry(frameEntry, bg="lightgrey", textvariable=descripcion)
entryDescripcion.grid(row="1", column="1", pady=5, padx=5)

usuario = StringVar()
label1 = Label(frameEntry, text="Usuario:")
label1.grid(row="2", column="0", sticky="e", pady=5, padx=5)
cuadroTexto1 = Entry(frameEntry, bg="lightgrey", textvariable=usuario)
cuadroTexto1.grid(row="2", column="1", pady=5, padx=5)

password = StringVar()
label2 = Label(frameEntry, text="Password:")
label2.grid(row="3", column="0", sticky="e", pady=5, padx=5)
cuadroTexto2 = Entry(frameEntry, bg="lightgrey", textvariable=password)
cuadroTexto2.grid(row="3", column="1", pady=5, padx=5)
cuadroTexto2.config(show="*")

label3 = Label(frameEntry, text="Comentarios:")
label3.grid(row="4", column="0", sticky="e", pady=5, padx=5)
text3 = Text(frameEntry, width="20", height="5")
text3.grid(row="4", column="1", pady="5", padx="5")
scroll3 = Scrollbar(frameEntry, command=text3.yview)
scroll3.grid(row="4", column="2", sticky="nsew")
text3.config(yscrollcommand=scroll3.set)


# Creamos frame en el que colocar los botones CRUD
frameButtons = Frame(root, width="500", height="100", bg="grey")
frameButtons.pack()

# Creamos botones de acción CRUD
botonClean = Button(frameButtons, text="Limpiar", command=boton)
botonClean.grid(row=0, column=0, pady=5, padx=5)

botonCreate = Button(frameButtons, text="Create", command=boton)
botonCreate.grid(row=0, column=1, pady=5, padx=5)

botonRead = Button(frameButtons, text="Read", command=boton)
botonRead.grid(row=0, column=2, pady=5, padx=5)

botonUpdate = Button(frameButtons, text="Update", command=boton)
botonUpdate.grid(row=0, column=3, pady=5, padx=5)

botonDelete = Button(frameButtons, text="Delete", command=boton)
botonDelete.grid(row = 0, column = 4, pady = 5, padx = 5)


root.mainloop()
