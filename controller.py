from random import sample
from conect import Conexion
import os

db = Conexion()

#Listar usuarios y saber cantidad de usuarios para asi mismo realizar la tabla
def listarUsuarios():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM users ORDER BY idUSer ASC"
    cursor.execute(sql)
    row=cursor.fetchall()
    lenght=len(row)#consulta la longitud de datos
    cursor.close()
    return row;

#Listar supervisores
def listarSupervisores():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM users WHERE typeUserId = '2'"
    cursor.execute(sql)
    row=cursor.fetchall()
    lenght=len(row)#consulta la longitud de datos
    cursor.close()
    return row;   

#Listar supervisores
def listarTecnicos():
    cursor = db.connection.cursor()
    sql = "SELECT * FROM users WHERE typeUserId = '3'"
    cursor.execute(sql)
    row=cursor.fetchall()
    lenght=len(row)#consulta la longitud de datos
    cursor.close()
    return row;   

#controlador para tecnicos cuando un tecnico crea un trabajo
def listarTrabajosCreadosTec(idUser):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM works WHERE idUserTec = ?", (idUser))
    row=cursor.fetchall()
    lenght=len(row)#consulta la longitud de datos
    cursor.close()
    return row;  
 
#controlador para supervisores cuando un supervisor crea un trabajo
def listarTrabajosCreadosSup(idUser):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM works WHERE idUserSup = ?", (idUser))
    row=cursor.fetchall()
    lenght=len(row)#consulta la longitud de datos
    cursor.close()
    return row;   
    
    
def createWorksTecn(idUser, idsupervisor, enableWork, typework, ubication, date, nameDoc, pathDoc):
    cursor = db.connection.cursor()
    sql = ("INSERT INTO works (idUserTec,idUserSup, enableWork, typeWork, ubicacion, dateWork, nameDoc, pathDoc)" 
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    cursor.execute(sql, (idUser, idsupervisor, enableWork, typework, ubication, date, nameDoc, pathDoc  )) #tupla
    db.connection.commit()
    cursor.close()
    return True

def createWorksSup(idUser, idtecnico, checkSup, typework, ubication, date, nameDoc, pathDoc):
    cursor = db.connection.cursor()
    sql = ("INSERT INTO works (idUserSup, idUserTec, checkSup, typeWork, ubicacion, dateWork, nameDoc, pathDoc )" 
           "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    cursor.execute(sql, (idUser, idtecnico, checkSup, typework, ubication, date, nameDoc, pathDoc  )) #tupla
    db.connection.commit()
    cursor.close()
    return True

def createDocsWork(nameDoc, pathDoc):
        cursor = db.connection.cursor()
        sql = ("INSERT INTO works (nameDoc, pathDoc)" 
           "VALUES (?, ?)")
        cursor.execute(sql, (nameDoc, pathDoc)) #tupla
        db.connection.commit()
        cursor.close()
        return True

#seleccionar el id del usuario para abrir el front con la información traida de la bd
def updateUser(idUser):
    cursor = db.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE idUser = '%s'" % (idUser))
    resultQuery=cursor.fetchone() #Devolviendo solo 1 registro
    cursor.close()
    return resultQuery

#recibeactualizar  
def getUpdates(name, lastname, typeUserId, username, email, photo, idUser):
    cursor = db.connection.cursor()
    sql = """UPDATE users SET
            name = ?,
            lastname = ?,
            typeUserId = ?,
            username = ?,
            mail = ?,
            photo = ?
            WHERE idUser=?"""
    cursor.execute(sql, (name, lastname, typeUserId, username, email, photo, idUser))
    db.connection.commit()
    cursor.close()
    return True

#recibe actualizar pero sin cambiar foto de perfil
def getUpdates2(name, lastname, typeUserId, username, email, idUser):
    cursor = db.connection.cursor()
    sql = """UPDATE users SET
            name = ?,
            lastname = ?,
            typeUserId = ?,
            username = ?,
            mail = ?
            WHERE idUser=?"""
    cursor.execute(sql, (name, lastname, typeUserId, username, email, idUser))
    db.connection.commit()
    cursor.close()
    return True

#Query para crear usuarios 
def createUser(name, lastname, hashed_password, typeUserId, username, mail, photo):
        cursor = db.connection.cursor()
        sql = ("INSERT INTO users (name, lastname, password, typeUserId, username, mail, photo)" 
           "VALUES (?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, (name, lastname, hashed_password, typeUserId, username, mail, photo)) #tupla
        db.connection.commit()
        cursor.close()
        return True

#Query para visualizar usuario en deltalle
def detallesdelusuario(idUser):
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE idUser = '%s'" % (idUser))
        resultQuery = cursor.fetchone()
        cursor.close() #cerrando conexion de la consulta sql
        return resultQuery

#metodo para eliminar usuario, se pasa data para traer la foto y se concatena con la 
#ruta para remover la foto

def deleteUser(idUser, data):
        rutaphoto = 'C:/Users/win10/workspaces/moduloSST/src/static/' + data.photo
        os.remove (rutaphoto)
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM users WHERE idUser = ?", (idUser,))
        db.connection.commit()
        cursor.close()
        return True
    
#Crear un string aleatorio para renombrar la foto 
# y evitar que exista una foto con el mismo nombre
def stringAleatorio():
    stringAleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = stringAleatorio.upper()
    resultadoAleatorio  = sample(secuencia, longitud)
    stringAleatorio     = "".join(resultadoAleatorio)
    return stringAleatorio

#Query para crear documentos en BD
def createDocs(nameDoc, pathDoc, enableDoc):
        cursor = db.connection.cursor()
        sql = ("INSERT INTO documents (nameDoc, pathDoc, enableDoc)" 
           "VALUES (?, ?, ?)")
        cursor.execute(sql, (nameDoc, pathDoc, enableDoc)) #tupla
        db.connection.commit()
        cursor.close()
        return True