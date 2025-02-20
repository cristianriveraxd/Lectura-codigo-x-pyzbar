
from conect import Conexion

db = Conexion()

#Obtener codigo de barras
def obtener_codigo_barras():
    cursor = db.connection.cursor()
    sql = ""  
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    
    if row:
        return row[0]  
    else:
        return None  
