# pylint: disable=all
import sqlite3
import os


ruta = os.path.join(os.path.dirname(__file__), "Bd_juegos.db")

class Database_juego:
    def __init__(self):
        self.conn = sqlite3.connect(ruta)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Juegos(
                            Nombre TEXT PRIMARY KEY,
                            Img BLOB NOT NULL,
                            Dispositivo TEXT NOT NULL,
                            Peso TEXT NOT NULL,
                            Descripcion TEXT NOT NULL,
                            Genero TEXT NOT NULL,
                            Link TEXT NOT NULL
                            )""")
        self.conn.commit()

    def buscar(self, nombre):
        self.cursor.execute("SELECT * FROM Juegos WHERE Nombre LIKE ?", ('%' + nombre + '%',))
        datos_encontrados = self.cursor.fetchall()
        return datos_encontrados
    
    def obtener_datos_juegos(self):
        try:
            self.cursor.execute("SELECT * FROM Juegos LIMIT 20")
            juegos = self.cursor.fetchall()
            return juegos
        except sqlite3.Error as e:
            print("Error al obtener datos de juegos:", e)
            return []
        
    def paginacion(self, number_page, datos_pagina):
        offset = (number_page - 1) * datos_pagina
        self.cursor.execute("SELECT * FROM Juegos LIMIT ? OFFSET ?",
                            (datos_pagina, offset))
        juegoscollector = self.cursor.fetchall()
        return juegoscollector
    
    def obtener_detalles_elemento_seleccionado(self,nombre_juego):
        detalles = {}
        try:
            
            self.cursor.execute("SELECT * FROM Juegos WHERE nombre = ?", (nombre_juego,))
            resultado = self.cursor.fetchone()

            if resultado:
                detalles['nombre'] = resultado[0]
                detalles['imagen'] = resultado[1]
                detalles['dispositivo'] = resultado[2]
                detalles['peso'] = resultado[3]
                detalles['descripcion'] = resultado[4]
                detalles['genero'] = resultado[5]
                detalles['link'] = resultado[6]
            self.conn.close()  # Cierras la conexión aquí

        except sqlite3.Error as e:
            print("Error al obtener detalles:", e)

        return detalles
    
    def filtrado(self, genero):
        self.cursor.execute("SELECT * FROM Juegos WHERE genero = ?", (genero,))
        juegos_genero = self.cursor.fetchall()
        return juegos_genero

if __name__ == '__main__':
    db = Database_juego()