# pylint: disable=all
import sqlite3
import os


ruta = os.path.join(os.path.dirname(__file__), "Bd_cursos.db")

class Database_cursos:
    def __init__(self):
        self.conn = sqlite3.connect(ruta)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS cursos(
                            Nombre TEXT PRIMARY KEY,
                            Img BLOB NOT NULL,
                            Descripcion TEXT NOT NULL,
                            genero TEXT NOT NULL,
                            Link TEXT NOT NULL
                            )""")
        self.conn.commit()

    def buscar(self, nombre):
        self.cursor.execute("SELECT * FROM cursos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        datos_encontrados = self.cursor.fetchall()
        return datos_encontrados

    def obtener_datos_juegos(self):
        try:
            self.cursor.execute("SELECT * FROM cursos LIMIT 20")
            juegos = self.cursor.fetchall()
            return juegos
        except sqlite3.Error as e:
            print("Error al obtener datos de cursos:", e)
            return []

    def paginacion(self, number_page, datos_pagina):
        offset = (number_page - 1) * datos_pagina
        self.cursor.execute("SELECT * FROM cursos LIMIT ? OFFSET ?",
                            (datos_pagina, offset))
        juegoscollector = self.cursor.fetchall()
        return juegoscollector

    def obtener_detalles_elemento_seleccionado(self,nombre_cursos):
        detalles = {}
        try:

            self.cursor.execute("SELECT * FROM cursos WHERE nombre = ?", (nombre_cursos,))
            resultado = self.cursor.fetchone()

            if resultado:
                detalles['nombre'] = resultado[0]
                detalles['imagen'] = resultado[1]
                detalles['descripcion'] = resultado[2]
                detalles['genero'] = resultado[3]
                detalles['link'] = resultado[4]
            self.conn.close()  # Cierras la conexión aquí

        except sqlite3.Error as e:
            print("Error al obtener detalles:", e)

        return detalles

    def filtrado(self, genero):
        self.cursor.execute("SELECT * FROM cursos WHERE genero = ?", (genero,))
        juegos_genero = self.cursor.fetchall()
        return juegos_genero

    def leer_imagen(self, Img):
        with open(Img, 'rb') as imagen:
            imagen_binario = imagen.read()
            return imagen_binario

if __name__ == '__main__':
    db = Database_cursos()
