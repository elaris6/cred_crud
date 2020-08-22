import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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

