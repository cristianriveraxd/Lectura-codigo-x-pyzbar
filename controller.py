
from conect import Conexion

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

