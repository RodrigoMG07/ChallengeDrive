# -*- coding: utf-8 -*-

import sqlite3


class FileDB:
    """ Esta clase posee los métodos necesarios para tratar los archivos provenientes de la unidad Drive de un usuario
    en una Base de Datos. """

    def __init__(self):
        pass

    def create_db(self):
        """ Creación de la Base de Datos. Se creará la tabla 'files_db' en la Base de Datos 'challenge_drive_db', la cual
            almacenerá los archivos de la unidad Drive del usuario con los campos: id, id_file, name, extension, owner,
            visibility, date_last_mod, flag public. Este último campo será 'True' para un registro en caso de que el
            archivo haya tenido alguna vez visibilidad 'publico'. Caso contrario, tendrá el valor 'False'. """

        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS files_db(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_file VARCHAR(100) NOT NULL,
        name VARCHAR(50) NOT NULL,
        extension VARCHAR(10) NOT NULL,
        owner VARCHAR(50) NOT NULL,
        visibility VARCHAR(10) NOT NULL,
        date_last_mod DATETIME NOT NULL,
        flag_public BOOLEAN NOT NULL)
        """
        if(consulta.execute(sql)):
            print('Tabla creada con éxito')
        else:
            print('Ha ocurrido un error al crear la tabla')
        consulta.close()
        conexion.commit()
        conexion.close()


    def insert_file(self,id_archivo,nombre_archivo,extension,owner,visibilidad,fecha_mod, flag_publico):
        # Inserta en la tabla 'files_db' un nuevo registro.

        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        argumentos = (id_archivo, nombre_archivo,extension,owner,visibilidad,fecha_mod, flag_publico)
        sql = """
        INSERT INTO files_db(id_file, name ,extension ,owner ,visibility ,date_last_mod, flag_public)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        if (consulta.execute(sql, argumentos)):
            print('Registro guardado con éxito')
        else:
            print('Ha ocurrido un error al guardar el registro')
        consulta.close()
        conexion.commit()
        conexion.close()


    def print_files(self):
        """ Imprime todos los archivos almacenados en la tabla 'files_db' con los siguientes datos: name, extension,
            owner, visibility y date_last_mod. """

        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql = """ SELECT * FROM files_db  """
        if (consulta.execute(sql)):
            filas = consulta.fetchall()
            print("Los archivos almacenados en la Base de Datos son: ")
            for fila in filas:
                print("""
                Nombre del archivo: %s
                Extensión del archivo: %s
                Owner del archivo: %s
                Visibilidad del archivo: %s
                Fecha de última modificación del archivo: %s
                """ % (fila[2], fila[3], fila[4], fila[5], fila[6]))
        consulta.close()
        conexion.commit()
        conexion.close()


    def exists_file(self, id_par):
        """ Retorna 'True' en caso de que el archivo con id 'id_par' exista dentro de la Base de Datos.
            Caso contrario retorna 'False'. """

        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql = """ SELECT * FROM files_db WHERE id_file = '%s' """ % (id_par)
        consulta.execute(sql)
        file = consulta.fetchone()
        consulta.close()
        conexion.commit()
        conexion.close()
        if file != None:
            return True
        else:
            return False

    def get_file(self, id_par):
        """ Retorna el archivo de la Base de Datos con id 'id_par' """
        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql = """ SELECT * FROM files_db WHERE id_file = '%s' """ % (id_par)
        consulta.execute(sql)
        file = consulta.fetchone()
        consulta.close()
        conexion.commit()
        conexion.close()
        return file

    def update_file(self, file):
        """ Actualiza los campos del archivo cargado como parámetro en la Base de Datos. """
        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql= """ 
        UPDATE files_db SET
        name = '%s',
        extension = '%s',
        owner = '%s',
        visibility = '%s',
        date_last_mod = '%s',
        flag_public = '%s'
        WHERE id_file = '%s'
        """ % (file[0], file[1], file[2], file[3], file[4], file[5], file[6])
        consulta.execute(sql)
        consulta.close()
        conexion.commit()
        conexion.close()
        return print("Se actualizó correctamente el archivo en la Base de Datos")

    def list_public_files(self):
        """ Lista todos los archivos de la Base de Datos que fueron alguna vez públicos """
        conexion = sqlite3.connect("sqlite3/challenge_drive_db.sqlite3")
        consulta = conexion.cursor()
        sql = """ SELECT * FROM files_db WHERE flag_public = 1 """
        consulta.execute(sql)
        publicFiles = consulta.fetchall()
        consulta.close()
        conexion.commit()
        conexion.close()
        return publicFiles

