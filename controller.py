
from conect import Conexion

db = Conexion()

#Obtener codigo de barras
def obtener_codigo_barras():
    cursor = db.connection.cursor()
    sql = "SELECT PRODUCTO FROM CONFIGURACION_LINEA WHERE LINEA = 3"  
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    return row
    
