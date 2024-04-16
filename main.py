import sys
from src.contactos import GestorContactos, Contacto
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy, QMessageBox,QInputDialog 
from src.utils.db_connection import conn


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gestor_contactos = GestorContactos(conn)
        self.search_results = QTableWidget(0, 5)
        self.contacto_temporal = None

        # Inicializar los campos de entrada
        self.input_nombre = QLineEdit(self)
        self.input_apellido = QLineEdit(self)
        self.input_telefono = QLineEdit(self)
        self.input_email = QLineEdit(self)
        self.input_direccion = QTextEdit(self)
        
        self.setWindowTitle("GESTOR DE CONTACTOS - APP ESAN")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Apellido", "Teléfono", "Email", "Dirección"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

            # Configurar la selección de filas en la tabla
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.create_main_panel()

        # Cambiar la señal a itemSelectionChanged
        self.table.itemSelectionChanged.connect(self.fill_contact_fields)

    def create_main_panel(self):
        self.clear_layout()

        self.panel_label = QLabel("APP DE GESTIÓN DE CONTACTOS", self)
        self.panel_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333; margin-bottom: 20px; text-align: center;")
        self.layout.addWidget(self.panel_label)

        # Botones principales con política de tamaño preferido
        self.button_insertar = QPushButton("Insertar Contacto", self)
        self.button_insertar.setStyleSheet("font-size: 16px;")
        self.button_insertar.clicked.connect(self.show_insertar_panel)
        self.button_insertar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addWidget(self.button_insertar)

        self.button_editar = QPushButton("Editar Contacto", self)
        self.button_editar.setStyleSheet("font-size: 16px;")
        self.button_editar.clicked.connect(self.show_editar_panel)
        self.button_editar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addWidget(self.button_editar)

        self.button_borrar = QPushButton("Borrar Contacto", self)
        self.button_borrar.setStyleSheet("font-size: 16px;")
        self.button_borrar.clicked.connect(self.show_borrar_panel)
        self.button_borrar.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addWidget(self.button_borrar)

        self.button_imprimir_csv = QPushButton("Imprimir CSV", self)
        self.button_imprimir_csv.setStyleSheet("font-size: 16px;")
        self.button_imprimir_csv.clicked.connect(self.imprimir_csv)
        self.button_imprimir_csv.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.layout.addWidget(self.button_imprimir_csv)

    
    def fill_contact_fields(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            nombre = self.table.item(row, 0).text()
            apellido = self.table.item(row, 1).text()
            telefono = self.table.item(row, 2).text()
            email = self.table.item(row, 3).text()
            direccion = self.table.item(row, 4).text()

            self.input_nombre.setText(nombre)
            self.input_apellido.setText(apellido)
            self.input_telefono.setText(telefono)
            self.input_email.setText(email)
            self.input_direccion.setPlainText(direccion)


    def fill_edit_fields(self):
        selected_items = self.search_results.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            nombre = self.search_results.item(row, 0).text()
            apellido = self.search_results.item(row, 1).text()
            telefono = self.search_results.item(row, 2).text()
            email = self.search_results.item(row, 3).text()
            direccion = self.search_results.item(row, 4).text()

            self.input_nombre.setText(nombre)
            self.input_apellido.setText(apellido)
            self.input_telefono.setText(telefono)
            self.input_email.setText(email)
            self.input_direccion.setPlainText(direccion)

            # Actualizar el contacto temporal
            self.contacto_temporal = Contacto(nombre, apellido, telefono, email, direccion)




    def show_insertar_panel(self):
        self.clear_layout()

        self.panel_label.setText("Insertar Contacto")
        self.layout.addWidget(self.panel_label)

        self.input_nombre = QLineEdit(self)
        self.input_nombre.setPlaceholderText("Nombre")
        self.layout.addWidget(self.input_nombre)

        self.input_apellido = QLineEdit(self)
        self.input_apellido.setPlaceholderText("Apellido")
        self.layout.addWidget(self.input_apellido)

        self.input_telefono = QLineEdit(self)
        self.input_telefono.setPlaceholderText("Teléfono")
        self.layout.addWidget(self.input_telefono)

        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Email")
        self.layout.addWidget(self.input_email)

        self.input_direccion = QTextEdit(self)
        self.input_direccion.setPlaceholderText("Dirección")
        self.layout.addWidget(self.input_direccion)

        self.button_agregar = QPushButton("Agregar", self)
        self.button_agregar.clicked.connect(self.agregar_contacto)
        self.layout.addWidget(self.button_agregar)

        self.button_volver = QPushButton("Volver", self)
        self.button_volver.clicked.connect(self.create_main_panel)
        self.layout.addWidget(self.button_volver)

    def agregar_contacto(self):
        # Obtener el texto de los campos de entrada
        nombre = self.input_nombre.text().strip()  # Elimina espacios en blanco al inicio y al final
        apellido = self.input_apellido.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        direccion = self.input_direccion.toPlainText().strip()

        # Realizar validaciones
        if not nombre:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un nombre válido.")
            return
        if not apellido:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un apellido válido.")
            return
        if not telefono.isdigit():  # Verifica que el teléfono solo contenga dígitos
            QMessageBox.warning(self, "Error", "Por favor, ingresa un teléfono válido.")
            return
        if not email or "@" not in email or "." not in email:  # Verifica un formato básico de correo electrónico
            QMessageBox.warning(self, "Error", "Por favor, ingresa un correo electrónico válido.")
            return
        if not direccion:
            QMessageBox.warning(self, "Error", "Por favor, ingresa una dirección válida.")
            return

        # Crear un nuevo objeto de Contacto con los valores ingresados
        nuevo_contacto = Contacto(nombre, apellido, telefono, email, direccion)

        # Llamar al método agregar_contacto del GestorContactos para agregar el nuevo contacto a la base de datos
        self.gestor_contactos.agregar_contacto(nuevo_contacto)

        # Mostrar mensaje de éxito o realizar otras acciones según sea necesario
        QMessageBox.information(self, "Éxito", "Contacto agregado con éxito.")
        self.create_main_panel()

    
    def show_editar_panel(self):
        self.clear_layout()

        self.panel_label.setText("Editar Contacto")
        self.layout.addWidget(self.panel_label)

        # Agregar barra de búsqueda y botón de búsqueda
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar contacto")
        self.layout.addWidget(self.search_bar)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.search_contact)
        self.layout.addWidget(self.search_button)

        # Crear la tabla search_results
        self.search_results = QTableWidget(0, 5)
        self.search_results.setHorizontalHeaderLabels(["Nombre", "Apellido", "Teléfono", "Email", "Dirección"])
        self.search_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.search_results)

        # Conectar la señal itemSelectionChanged a fill_edit_fields
        self.search_results.itemSelectionChanged.connect(self.fill_edit_fields)

        # Configurar el texto de los campos de entrada a una cadena vacía
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setPlaceholderText("Nombre")
        self.layout.addWidget(self.input_nombre)

        self.input_apellido = QLineEdit(self)
        self.input_apellido.setPlaceholderText("Apellido")
        self.layout.addWidget(self.input_apellido)

        self.input_telefono = QLineEdit(self)
        self.input_telefono.setPlaceholderText("Teléfono")
        self.layout.addWidget(self.input_telefono)

        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Email")
        self.layout.addWidget(self.input_email)

        self.input_direccion = QTextEdit(self)
        self.input_direccion.setPlaceholderText("Dirección")
        self.layout.addWidget(self.input_direccion)
        

        self.button_editar = QPushButton("Editar", self)
        self.button_editar.clicked.connect(self.editar_contacto)
        self.layout.addWidget(self.button_editar)

        self.button_volver = QPushButton("Volver", self)
        self.button_volver.clicked.connect(self.create_main_panel)
        self.layout.addWidget(self.button_volver)



    def editar_contacto(self):
        # Verificar si se ha seleccionado un contacto para editar
        selected_items = self.search_results.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un contacto para editar.")
            return

        # Obtener el texto de los campos de entrada
        nombre = self.input_nombre.text().strip()
        apellido = self.input_apellido.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        direccion = self.input_direccion.toPlainText().strip()


        # Realizar validaciones
        if not nombre:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un nombre válido.")
            return
        if not apellido:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un apellido válido.")
            return
        if not telefono.isdigit():  # Verifica que el teléfono solo contenga dígitos
            QMessageBox.warning(self, "Error", "Por favor, ingresa un teléfono válido.")
            return
        if not email or "@" not in email or "." not in email:  # Verifica un formato básico de correo electrónico
            QMessageBox.warning(self, "Error", "Por favor, ingresa un correo electrónico válido.")
            return
        if not direccion:
            QMessageBox.warning(self, "Error", "Por favor, ingresa una dirección válida.")
            return

        # Crear un objeto Contacto actualizado con los valores ingresados
        contacto_editado = Contacto(nombre, apellido, telefono, email, direccion)

        self.gestor_contactos.editar_contacto(self.contacto_temporal, contacto_editado)


        # Mostrar mensaje de éxito o realizar otras acciones según sea necesario
        QMessageBox.information(self, "Éxito", "Contacto editado con éxito.")
        self.create_main_panel()

    
    def show_borrar_panel(self):
        self.clear_layout()

        self.panel_label.setText("Borrar Contacto")
        self.layout.addWidget(self.panel_label)

        # Agregando barra de búsqueda, botón de búsqueda y tabla de resultados
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Buscar contacto")
        self.layout.addWidget(self.search_bar)

        self.search_button = QPushButton("Buscar", self)
        self.search_button.clicked.connect(self.search_contact)
        self.layout.addWidget(self.search_button)

        self.search_results = QTableWidget(0, 5)
        self.search_results.setHorizontalHeaderLabels(["Nombre", "Apellido", "Teléfono", "Email", "Dirección"])
        self.search_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.search_results)

        # Conectar la señal itemSelectionChanged a fill_edit_fields para autocompletar los campos
        self.search_results.itemSelectionChanged.connect(self.fill_edit_fields)

        # Campos de entrada
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setPlaceholderText("Nombre")
        self.input_nombre.setEnabled(False)  # Deshabilitar campo
        self.layout.addWidget(self.input_nombre)

        self.input_apellido = QLineEdit(self)
        self.input_apellido.setPlaceholderText("Apellido")
        self.input_apellido.setEnabled(False)  # Deshabilitar campo
        self.layout.addWidget(self.input_apellido)

        self.input_telefono = QLineEdit(self)
        self.input_telefono.setPlaceholderText("Teléfono")
        self.input_telefono.setEnabled(False)  # Deshabilitar campo
        self.layout.addWidget(self.input_telefono)

        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Email")
        self.input_email.setEnabled(False)  # Deshabilitar campo
        self.layout.addWidget(self.input_email)

        self.input_direccion = QTextEdit(self)
        self.input_direccion.setPlaceholderText("Dirección")
        self.input_direccion.setEnabled(False)  # Deshabilitar campo
        self.layout.addWidget(self.input_direccion)

        self.button_eliminar = QPushButton("Eliminar Contacto", self)
        self.button_eliminar.clicked.connect(self.eliminar_contacto)
        self.layout.addWidget(self.button_eliminar)

        self.button_volver = QPushButton("Volver", self)
        self.button_volver.clicked.connect(self.create_main_panel)
        self.layout.addWidget(self.button_volver)


    def eliminar_contacto(self):
        # Verificar si se ha seleccionado un contacto para eliminar
        selected_items = self.search_results.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "Por favor, selecciona un contacto para eliminar.")
            return

        # Obtener el texto de los campos de entrada
        nombre = self.input_nombre.text().strip()
        apellido = self.input_apellido.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        direccion = self.input_direccion.toPlainText().strip()

        # Realizar validaciones
        if not nombre:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un nombre válido.")
            return
        if not apellido:
            QMessageBox.warning(self, "Error", "Por favor, ingresa un apellido válido.")
            return
        if not telefono.isdigit():  # Verifica que el teléfono solo contenga dígitos
            QMessageBox.warning(self, "Error", "Por favor, ingresa un teléfono válido.")
            return
        if not email or "@" not in email or "." not in email:  # Verifica un formato básico de correo electrónico
            QMessageBox.warning(self, "Error", "Por favor, ingresa un correo electrónico válido.")
            return
        if not direccion:
            QMessageBox.warning(self, "Error", "Por favor, ingresa una dirección válida.")
            return

        # Crear un objeto Contacto actualizado con los valores ingresados
        contacto = Contacto(nombre, apellido, telefono, email, direccion)
        self.gestor_contactos.eliminar_contacto(contacto)

        # Mostrar mensaje de éxito o realizar otras acciones según sea necesario
        QMessageBox.information(self, "Éxito", "Contacto eliminado con éxito.")
        self.create_main_panel()
    
    

    def imprimir_csv(self):
        nombre_archivo, ok = QInputDialog.getText(self, 'Nombre del archivo CSV', 'Ingrese un nombre para el archivo CSV:')
        if ok:
            self.gestor_contactos.exportar_csv(nombre_archivo)
    
    def search_contact(self):
        search_text = self.search_bar.text().strip().lower()
    
        if search_text:
            # Buscar en la base de datos o en los datos cargados en la tabla
            # Por ahora, supongamos que tenemos los datos en la lista self.lista_contactos
            resultados = []
            for contacto in self.gestor_contactos.obtener_contactos():
                if search_text in contacto.nombre.lower() or search_text in contacto.apellido.lower() or search_text in contacto.telefono.lower() or search_text in contacto.email.lower() or search_text in contacto.direccion.lower():
                    resultados.append(contacto)

            # Limpiar la tabla de resultados
            self.search_results.setRowCount(0)

            # Llenar la tabla de resultados con los resultados de la búsqueda
            for row, contacto in enumerate(resultados):
                self.search_results.insertRow(row)
                self.search_results.setItem(row, 0, QTableWidgetItem(contacto.nombre))
                self.search_results.setItem(row, 1, QTableWidgetItem(contacto.apellido))
                self.search_results.setItem(row, 2, QTableWidgetItem(contacto.telefono))
                self.search_results.setItem(row, 3, QTableWidgetItem(contacto.email))
                self.search_results.setItem(row, 4, QTableWidgetItem(contacto.direccion))

            # Ajustar automáticamente el tamaño de las columnas para que se ajusten al contenido
            self.search_results.resizeColumnsToContents()

            # Mostrar la tabla de resultados y ocultar la tabla principal
            self.search_results.setVisible(True)
            self.table.setVisible(False)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa un término de búsqueda válido.")

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
