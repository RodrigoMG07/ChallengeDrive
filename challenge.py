# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
from gmail import send_mail
from file_DB import FileDB

total_files = []

def list_files():
    """ Recorre todos los archivos del Google Drive de un usuario (max 999) y retorna una lista
    con los archivos almacenados """

    results = service.files().list(pageSize=999,  fields='nextPageToken, files(id, name, fileExtension, '
                                                           'modifiedTime, mimeType, owners, permissions, '
                                                         'permissionIds)',
                                                    q="mimeType != 'application/vnd.google-apps.folder'").execute()
    items = results.get('files', [])
    drive_Files = []
    if not items:
        print('No se encontraron archivos.')
    else:
        for item in items:
            drive_Files.append(item)
        print('Total de archivos encontrados =', len(items))
        print(' ')
    return drive_Files

def remove_permission(service, fileId, permissionId):
    """ Elimina del archivo con ID 'fileId' el permiso almacenado en 'permissionId'. Será utilizado para remover la
        propiedad pública del archivo """
    try:
        service.permissions().delete(fileId=fileId, permissionId=permissionId).execute()
        print('Se eliminó la propiedad pública del archivo')
    except errors.HttpError as error:
        print('Ocurrió un error: %s' % error)

def compare_files(fileDB, file_drive):
    """ Compara los campos de las listas fileDB y file_drive. En caso de que todos los campos de ambas listas
        sean iguales, indicaría que no hubo modificaciones entre el archivo de la unidad Drive y el mismo archivo
        almacenado en la BD, por lo que la función retorna True. Caso contrario, retorna False. """

    if (fileDB[2] == file_drive[0] and fileDB[3] == file_drive[1] and fileDB[4] == file_drive[2]
            and fileDB[5] == file_drive[3] and fileDB[6] == file_drive[4]):
        return True
    else:
        return False

if __name__ == '__main__':
    # Cuerpo principal del programa

    """ Configuración de los valores básicos de la API Google Drive, donde se definen el alcance (SCOPE) y 
    el tratamiendo de credenciales del usuario"""
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    """ Generación de la lista 'totalFile' que contendrá todos los archivos de Google Drive del usuario. """
    total_files = list_files()

    """ Creación de una instancia de la clase 'FileDB'. """
    file_inst = FileDB()

    """ Creación la Base de Datos. """
    file_inst.create_db()

    for file in total_files:
        """ Determina la extensión del archivo. En caso de que el mismo no posea el campo 'fileExtension', indicaría
            que el archivo fue creado desde una unidad Drive. """
        if 'fileExtension' in file:
            ext = file['fileExtension']
        else:
            ext = 'drive'

        """ Almacena en 'name' el nombre del archivo. """
        name = file['name'].split('.')
        name = name[0]

        """ Corrobora si el archivo existe o no en la Base de Datos creada previamente. En caso de no existir, ingresa
            un nuevo registro en la BD si posee los suficientes permisos. Caso contrario, verifica si se realizó alguna
            modificación en el archivo y realiza la correspondiente actualización en la Base de Datos. """
        if file_inst.exists_file(file['id']) == False:
            print(" ")
            print('Procederemos a cargar un nuevo archivo: ', name)
            message = """ *** Se modificó la visibilidad de 'público' a 'privado' del siguiente archivo: ***
            
                            Nombre: %s
                            Extension: %s
                            Fecha de última modificacion: %s
                            Owner: %s
                            Visibilidad: %s
                         """ % (file['name'], ext, file['modifiedTime'], file['owners'][0]['displayName'], 'privado')
            if 'permissions' and 'permissionIds' in file:
                """ Determina si el archivo posee visibilidad pública (pública general o pública mediante link). """
                if ('anyone' in file['permissionIds']) or ('anyoneWithLink' in file['permissionIds']):
                    if 'anyone' in file['permissionIds']:
                        remove_permission(service, file['id'], 'anyone')
                    else:
                        remove_permission(service, file['id'], 'anyoneWithLink')
                    """ En ambos casos se elimina el permiso de visilibidad 'público' y se envía un correo al owner del
                        archivo notificando el cambio. Se setea una flag en True para determinar que el archivo fue 
                        público en algún momento. """
                    send_mail(message, file['owners'][0]['emailAddress'])
                    flag_vis = 1
                else:
                    flag_vis = 0
                """ Inserta el archivo con los datos pertinentes en la Base de Datos. """
                file_inst.insert_file(file['id'], name, ext, file['owners'][0]['displayName'], 'privado',
                                      file['modifiedTime'], flag_vis)
            else:
                print('No se puede almacenar este archivo en la Base de Datos debido a que carece de permisos '
                      'suficientes para el usuario.')
                print(" ")
        else:
            print('El archivo con nombre "', name, '" ya se encuentra cargado en la BD')
            print('Procederemos a verificar si se realizó alguna modificación en el archivo')

            if 'permissionIds' in file:
                """ Obtiene mediante el 'id' el archivo existente creado en la Base de Datos. """
                one_file = file_inst.get_file(file['id'])

                """ Obtiene la visibilidad actual que posee el archivo en la unidad Drive. """
                if ('anyone' in file['permissionIds']) or ('anyoneWithLink' in file['permissionIds']):
                    visibility = 'publico'
                    flag_vis = 1
                else:
                    visibility = 'privado'
                    """ Si el 'flag_public' estaba en False, quedará con el mismo valor. Caso contrario, su
                        valor quedará en 1 para que figure en el historial de archivos con visibilidad 'publica'. """
                    if one_file[7] == 0:
                        flag_vis = 0
                    else:
                        flag_vis = 1

                """ Crea una lista 'file_drive' con los valores actuales del archivo de la unidad Drive. """
                file_drive = [name, ext, file['owners'][0]['displayName'], visibility, file['modifiedTime'], flag_vis,
                             file['id']]

                """ Compara los campos del archivo existente en la Base de Datos con los campos del archivo del Drive
                    para determinar si el archivo sufrió modificaciones o no. """
                if compare_files(one_file, file_drive):
                    print('El archivo NO sufrió modificaciones')
                else:
                    print('El archivo SI sufrió modificaciones, procederemos a actualizar sus valores.')

                    """ Actualiza el archivo existente de la Base de Datos con los nuevos valores del mismo archivo 
                        contenido en la unidad Drive del usuario. """
                    file_inst.update_file(file_drive)
                print(" ")
            else:
                print('El archivo NO sufrió modificaciones o se le han quitado los permisos de edición.')
                print(" ")
    print(" ")

    """ Muestra aquellos archivos que hayan tenido visibilidad 'publico' en algún momento, sin importar la visibilidad 
    que posean actualmente. """
    answer = input('¿Desea listar el histórico de archivos públicos? ')
    historic = file_inst.list_public_files()
    if answer == 'si' or answer == 's':
        if historic != []:
            print('El historial de los archivos que fueron alguna vez públicos son: ')
            for i in historic:
                print(" ")
                print('Nobre del archivo: ', i[2])
                print('Extensión del archivo:', i[3])
                print('Owner del archivo: ', i[4])
                print('Fecha de última modificación: ', i[6])
        else:
            print('No existen archivos que hayan tenido visibilidad "público" en algún momento.')

    """ Muestra aquellos archivos almacenados en la Base de Datos. """
    print(" ")
    answer = input('¿Desea listar los archivos almacenados en la Base de Datos? ')
    if answer == 'si' or answer == 's':
        file_inst.print_files()


