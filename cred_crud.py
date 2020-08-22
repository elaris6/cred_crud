import sqlite3
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

conexion_bbdd = sqlite3.connect("cred_crud.db")
cursor_bbdd = conexion_bbdd.cursor()




cursor_bbdd.close()
conexion_bbdd.close()
