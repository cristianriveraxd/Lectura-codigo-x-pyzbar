import pyodbc

class Conexion:
    def __init__(self):
        try:
            self.connection = pyodbc.connect('DRIVER={SQL Server};SERVER=CRISTIAN\SQLEXPRESS01;DATABASE=DB_MODULO;Trusted_Connection=yes')
            print('Conexión exitosa')
        except Exception as e:
            print(e)

