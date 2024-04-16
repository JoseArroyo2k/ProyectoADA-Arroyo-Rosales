# src/contactos.py
import csv
import pyodbc
import os

class Contacto:
    def __init__(self, nombre, apellido, telefono, email, direccion):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    def __str__(self):
        return f"{self.nombre} {self.apellido} - Teléfono: {self.telefono}, Email: {self.email}, Dirección: {self.direccion}"

class GestorContactos:
    def __init__(self, connection):
        self.connection = connection

    def agregar_contacto(self, contacto):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Contactos (nombre, apellido, telefono, email, direccion) VALUES (?, ?, ?, ?, ?)",
                           (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email, contacto.direccion))
            self.connection.commit()
            cursor.close()
            print("Contacto agregado correctamente a la base de datos.")
        except pyodbc.Error as e:
            print(f"Error al agregar el contacto a la base de datos: {e}")


    def editar_contacto(self, contacto_temporal, contacto_editado):
        try:
            cursor = self.connection.cursor()

            # Buscar el ID del contacto original en la base de datos
            cursor.execute("SELECT id_contacto FROM Contactos WHERE nombre=? AND apellido=? AND telefono=?",
                            (contacto_temporal.nombre, contacto_temporal.apellido, contacto_temporal.telefono))
            resultado = cursor.fetchone()

            if resultado:
                # Actualizar la entrada en la base de datos con el ID encontrado y los valores editados
                cursor.execute("UPDATE Contactos SET nombre=?, apellido=?, telefono=?, email=?, direccion=? WHERE id_contacto=?",
                                (contacto_editado.nombre, contacto_editado.apellido, contacto_editado.telefono, contacto_editado.email, contacto_editado.direccion, resultado[0]))
                self.connection.commit()
                cursor.close()
                print("Contacto editado correctamente en la base de datos.")
            else:
                print("No se encontró ningún contacto con los datos proporcionados:")
                print("Contacto Temporal:")
                print(f"Nombre: {contacto_temporal.nombre}")
                print(f"Apellido: {contacto_temporal.apellido}")
                print(f"Teléfono: {contacto_temporal.telefono}")
                print(f"Email: {contacto_temporal.email}")
                print(f"Dirección: {contacto_temporal.direccion}")
                print("Contacto Actualizado:")
                print(f"Nombre: {contacto_editado.nombre}")
                print(f"Apellido: {contacto_editado.apellido}")
                print(f"Teléfono: {contacto_editado.telefono}")
                print(f"Email: {contacto_editado.email}")
                print(f"Dirección: {contacto_editado.direccion}")

        except pyodbc.Error as e:
            print(f"Error al editar el contacto en la base de datos: {e}")

    '''
    def editar_contacto(self, contacto):
        try:
            cursor = self.connection.cursor()

            # Buscar el ID del contacto que coincida con los parámetros proporcionados
            cursor.execute("SELECT id_contacto FROM Contactos WHERE nombre=? AND apellido=? AND telefono=?",
                            (contacto.nombre, contacto.apellido, contacto.telefono))
            resultado = cursor.fetchone()
            if resultado:
                # Actualizar la entrada en la base de datos
                cursor.execute("UPDATE Contactos SET nombre=?, apellido=?, telefono=?, email=?, direccion=? WHERE id_contacto=?",
                                (contacto.nombre, contacto.apellido, contacto.telefono, contacto.email, contacto.direccion, resultado[0]))
                self.connection.commit()
                cursor.close()
                print("Contacto editado correctamente en la base de datos.")
            else:
                print("No se encontró ningún contacto con los datos proporcionados.")

        except pyodbc.Error as e:
            print(f"Error al editar el contacto en la base de datos: {e}")
    '''


    def eliminar_contacto(self, contacto):
        try:
            cursor = self.connection.cursor()

            # Buscar el ID del contacto que coincida con los parámetros proporcionados
            cursor.execute("SELECT id_contacto FROM Contactos WHERE nombre=? AND apellido=? AND telefono=?",
                            (contacto.nombre, contacto.apellido, contacto.telefono))
            resultado = cursor.fetchone()
            if resultado:
                # Eliminar la entrada en la base de datos
                cursor.execute("DELETE FROM Contactos WHERE id_contacto=?", (resultado[0],))
                self.connection.commit()
                cursor.close()
                print("Contacto eliminado correctamente en la base de datos.")
            else:
                print("No se encontró ningún contacto con los datos proporcionados.")

        except pyodbc.Error as e:
            print(f"Error al eliminar el contacto en la base de datos: {e}")


    def obtener_contactos(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Contactos")
            contactos = []
            for row in cursor.fetchall():
                contacto = Contacto(row.nombre, row.apellido, row.telefono, row.email, row.direccion)
                contactos.append(contacto)
            cursor.close()
            return contactos
        except pyodbc.Error as e:
            print(f"Error al obtener los contactos de la base de datos: {e}")
            return []

    def exportar_csv(self, nombre_archivo):
        # Ruta donde se guardará el archivo CSV
        ruta_guardado = "C:/Users/José Arroyo/Desktop/CSVS EXPORTADOS/"
        # Concatenar el nombre del archivo proporcionado con la ruta de guardado
        nombre_completo = os.path.join(ruta_guardado, f"{nombre_archivo}.csv")
        
        contactos = self.obtener_contactos()
        with open(nombre_completo, 'w', newline='') as csvfile:
            fieldnames = ["Nombre", "Apellido", "Teléfono", "Email", "Dirección"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for contacto in contactos:
                # Asegúrate de que las claves del diccionario coincidan con fieldnames
                writer.writerow({
                    "Nombre": contacto.nombre,
                    "Apellido": contacto.apellido,
                    "Teléfono": contacto.telefono,
                    "Email": contacto.email,
                    "Dirección": contacto.direccion
                })
        print("PERRITO LOGRADO , SE LOGRO CSM")        
