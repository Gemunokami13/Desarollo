# pylint: disable=all
import sqlite3
import os

ruta = os.path.join(os.path.dirname(__file__), "Bd_peliculas.db")

class Database_pelis:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conection()

    def conection(self):
        self.conn = sqlite3.connect(ruta)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS peliculas(
                            Nombre TEXT PRIMARY KEY,
                            Img BLOB NOT NULL,
                            Peso TEXT NOT NULL,
                            Descripcion TEXT NOT NULL,
                            Genero TEXT NOT NULL,
                            Link TEXT NOT NULL,
                            contraseña TEXT
                            )""")
        self.conn.commit()

    def buscar(self, nombre):
        self.cursor.execute("SELECT * FROM peliculas WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        datos_encontrados = self.cursor.fetchall()
        return datos_encontrados

    def paginacion(self, number_page, datos_pagina):
        offset = (number_page - 1) * datos_pagina

        self.cursor.execute("SELECT * FROM peliculas LIMIT ? OFFSET ?",
                            (datos_pagina, offset))

        peliculas = self.cursor.fetchall()
        return peliculas

    def obtener_datos_peliculas(self):
        try:
            self.cursor.execute("SELECT * FROM peliculas LIMIT 20")
            peliculas = self.cursor.fetchall()
            return peliculas
        except sqlite3.Error as e:
            print("Error al obtener datos de peliculas:", e)
            return []

    def obtener_detalles_elemento_seleccionado(self,nombre_pelicula):
        detalles = {}
        try:

            self.cursor.execute("SELECT * FROM peliculas WHERE nombre = ?", (nombre_pelicula,))
            resultado = self.cursor.fetchone()

            if resultado:
                detalles['nombre'] = resultado[0]
                detalles['imagen'] = resultado[1]
                detalles['peso'] = resultado[2]
                detalles['Descripcion'] = resultado[3]
                detalles['Genero'] = resultado[4]
                detalles['Link'] = resultado[5]
                detalles['contraseña'] = resultado[6]
            self.conn.close()

        except sqlite3.Error as e:
            print("Error al obtener detalles:", e)

        return detalles

    def filtrado(self, genero):
        self.cursor.execute("SELECT * FROM peliculas WHERE genero = ?", (genero,))
        peliculas_genero = self.cursor.fetchall()
        return peliculas_genero

if __name__ == '__main__':
    db = Database_pelis()