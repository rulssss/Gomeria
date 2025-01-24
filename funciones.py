import psycopg2
from psycopg2 import errors
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import os
import sys
import json
import hashlib
import uuid

#################################################
#################################################
#################################################
#################################################

connection2 = psycopg2.connect(
host="localhost",
user="postgres",
password="Mariano302",
database="Gomeriadb",
port="5432"
)
# autocommit
connection2.autocommit = True

#################################################
#################################################
#################################################
#################################################



#####################################
# FUNCIONES PARA LOGIN db
#####################################

def registrar_usuario(username, password, account):

    if account == "Administrador":
        account = True
    else:
        account = False     #Aacomoda la variable account a un true o fals epara verificar que tipo de cuenta es

    cursor= connection2.cursor()
    query_data1 = f"INSERT INTO usuarios(nombre, contrasenia, admin, fecha_registro) VALUES('{username}', '{password}', {account}, '{datetime.now()}')"
    cursor.execute(query_data1)
    cursor.close()

def hay_admin():
    cursor= connection2.cursor()
    query_data = f"SELECT id_usuario FROM usuarios WHERE admin = True"
    cursor.execute(query_data)
    data = cursor.fetchall()
    cursor.close()

    if data == []: # verifica si hay algun administrador, si no hay devuelve false y abre la ventana de registro
        return False
    else:
        return True

def actualizar_contrasena(new_password, recover_id):
    cursor= connection2.cursor()
    query_data = f"UPDATE usuarios SET contrasenia = '{new_password}' WHERE id_usuario = {recover_id}"
    cursor.execute(query_data)
    cursor.close()


def existencia_de_id(recover_id):
    cursor= connection2.cursor()
    # 
    query_data = f"SELECT id_usuario FROM usuarios WHERE id_usuario = '{recover_id}'"
    cursor.execute(query_data)
    data = cursor.fetchall()
    cursor.close()

    

    if data != []:
        return True
    else:
        return False   
     

def existe_usuario(username):
    cursor= connection2.cursor()
    query_data = f"SELECT nombre FROM usuarios WHERE nombre = '{username}'"
    cursor.execute(query_data)
    data = cursor.fetchall()
    cursor.close()
    
    if data != []:
        return True
    else: 
        return False


def verificar_contrasenia(password, username, account):
    
    cursor= connection2.cursor()
    query_data2 = f"SELECT contrasenia, admin FROM usuarios WHERE nombre = '{username}'"
    cursor.execute(query_data2)
    data = cursor.fetchall()
    cursor.close()


    ###########ORDENAR PARA CORREGIR QUE VERIFIQUE SI ES USUARIO O ADMIN  ES DECIR, QUE VEA SI ES TRUE O FALSE EN LA TABLA APRA NO TRAER TODOS LOS NOBRES

    if account == "Administrador":
        account = True
    else:
        account = False     #Aacomoda la variable account a un true o false para verificar que tipo de cuenta es

    if data != []:
        if data[0][0] != password or data[0][1] != account: ## verifica password igual y si el tipo es igual al seleccionado
            return True # devuelve true si alguno es distinto para tirar el mensaje de error
    else:
        return False



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_user_data_path(filename):
    """ Get path to the user's data directory """
    user_data_dir = os.path.join(os.getenv('APPDATA'), 'MyApp')
    os.makedirs(user_data_dir, exist_ok=True)
    return os.path.join(user_data_dir, filename)