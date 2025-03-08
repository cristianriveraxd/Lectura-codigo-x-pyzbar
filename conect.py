import pyodbc

class Conexion:
    def __init__(self):
        try:
            self.connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=192.168.1.2;DATABASE=BDPASTADORIA;UID=CristianRivera;PWD=Doria_2022+;TrustServerCertificate=yes')
            print('Conexión exitosa')
        except Exception as e:
            print(e)

p = Conexion()
