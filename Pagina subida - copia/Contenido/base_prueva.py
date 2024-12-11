# pylint: disable=all
import sqlite3
import os


ruta = os.path.join(os.path.dirname(__file__), "Bd_lentes.db")

class Database_animes:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.conection()

    def conection(self):
        self.conn = sqlite3.connect(ruta)
        self.cursor = self.conn.cursor()
        #self.cursor.execute("""ALTER TABLE animes
                #ADD COLUMN contraseña TEXT""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lentes(
                            Nombre TEXT PRIMARY KEY,
                            Img BLOB NOT NULL,
                            Lenguaje NOT NULL,
                            Temporada INT NOT NULL,
                            Descripcion TEXT NOT NULL,
                            contenido TEXT NOT NULL,
                            Genero TEXT NOT NULL,
                            Link TEXT NOT NULL,
                            contraseña TEXT
                            )""")
        self.conn.commit()

    def leer_imagen(self, Img):
        with open(Img, 'rb') as imagen:
            imagen_binario = imagen.read()
            return imagen_binario

    def agregar(self, Nombre, Img, Lenguaje, Temporada, Descripcion, contenido, Genero, Link, contraseña):
        imagen_binario = self.leer_imagen(Img)

        self.cursor.execute("INSERT INTO animes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (Nombre, imagen_binario, Lenguaje, Temporada, Descripcion, contenido, Genero, Link, contraseña))
        self.conn.commit()

    def buscar(self, nombre):
        self.cursor.execute("SELECT * FROM animes WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        datos_encontrados = self.cursor.fetchall()
        return datos_encontrados

    
    def obtener_datos_animes(self):
        try:
            self.cursor.execute("SELECT * FROM animes LIMIT 20")
            animes = self.cursor.fetchall()
            return animes
        except sqlite3.Error as e:
            print("Error al obtener datos de animes:", e)
            return []

    def paginacion(self, number_page, datos_pagina):
        offset = (number_page - 1) * datos_pagina

        self.cursor.execute("SELECT * FROM animes LIMIT ? OFFSET ?",
                            (datos_pagina, offset))
        
        peliculas = self.cursor.fetchall()
        return peliculas
    
    def obtener_detalles_elemento_seleccionado(self, nombre_animes):
        detalles = {}
        try:
            self.cursor.execute("SELECT * FROM animes WHERE nombre = ?", (nombre_animes,))
            resultado = self.cursor.fetchone()

            # Verificar si se encontraron detalles
            if resultado:
                detalles['nombre'] = resultado[0] 
                detalles['imagen'] = resultado[1]
                detalles['Lenguaje'] = resultado[2]
                detalles['Temporada'] = resultado[3]
                detalles['Descripcion'] = resultado[4]
                detalles['contenido'] = resultado[5]
                detalles['Genero'] = resultado[6]
                detalles['Link'] = resultado[7]
                detalles['contraseña'] = resultado[8]

            self.conn.close()  # Cierras la conexión aquí

        except sqlite3.Error as e:
            print("Error al obtener detalles:", e)

        return detalles
    
    def filtrado(self, genero):
        self.cursor.execute("SELECT * FROM animes WHERE genero = ?", (genero,))
        peliculas_genero = self.cursor.fetchall()
        return peliculas_genero
    
    def eliminar(self, Nombre):
        self.cursor.execute("DELETE FROM animes WHERE Nombre = ?", (Nombre,))
        self.conn.commit()


    
if __name__ == '__main__':
    db = Database_animes()