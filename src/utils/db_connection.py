import pyodbc

# Parámetros de conexión
server = 'DESKTOP-I4S1736'  # Nombre del servidor SQL
database = 'GestorContactos'  # Nombre de la base de datos

# Cadena de conexión
connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=True'

# Establecer la conexión
try:
    conn = pyodbc.connect(connection_string)
    print("**Conexión generada correctamente al conectarte a la base de datos.**")
except pyodbc.Error as e:
    print(f"**Error al conectar a la base de datos: {e}**")
