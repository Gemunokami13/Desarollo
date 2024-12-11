# pylint: disable=all
import sqlite3
import os

ruta = os.path.join(os.path.dirname(__file__), "Bd_series.db")

class Database_series:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conection()

    def conection(self):
        self.conn = sqlite3.connect(ruta)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS series(
                            Nombre TEXT PRIMARY KEY,
                            Img BLOB NOT NULL,
                            Lenguaje NOT NULL,
                            Temporada INT NOT NULL,
                            Descripcion TEXT NOT NULL,
                            contenido TEXT NOT NULL,
                            Genero TEXT NOT NULL,
                            Link TEXT NOT NULL
                            )""")
        self.conn.commit()

    def buscar(self, nombre):
        self.cursor.execute("SELECT * FROM series WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        datos_encontrados = self.cursor.fetchall()
        return datos_encontrados
    
    def obtener_datos_series(self):
        try:
            self.cursor.execute("SELECT * FROM series LIMIT 20")
            series = self.cursor.fetchall()
            return series
        except sqlite3.Error as e:
            print("Error al obtener datos de series:", e)
            return []

    def paginacion(self, number_page, datos_pagina):
        offset = (number_page - 1) * datos_pagina

        self.cursor.execute("SELECT * FROM series LIMIT ? OFFSET ?",
                            (datos_pagina, offset))
        
        peliculas = self.cursor.fetchall()
        return peliculas
    
    def obtener_detalles_elemento_seleccionado(self,nombre_serie):
        detalles = {}
        try:

            self.cursor.execute("SELECT * FROM series WHERE nombre = ?", (nombre_serie,))
            resultado = self.cursor.fetchone()

            if resultado:
                detalles['nombre'] = resultado[0] 
                detalles['imagen'] = resultado[1]
                detalles['Lenguaje'] = resultado[2]
                detalles['Temporada'] = resultado[3]
                detalles['Descripcion'] = resultado[4]
                detalles['contenido'] = resultado[5]
                detalles['Genero'] = resultado[6]
                detalles['Link'] = resultado[7]
            self.conn.close()
        except sqlite3.Error as e:
            print("Error al obtener detalles:", e)

        return detalles
    
    def filtrado(self, genero):
        self.cursor.execute("SELECT * FROM series WHERE genero = ?", (genero,))
        peliculas_genero = self.cursor.fetchall()
        return peliculas_genero

if __name__ == '__main__':
    db = Database_series()