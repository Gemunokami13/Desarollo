# pylint: disable=all
import sqlite3
import os


ruta = os.path.join(os.path.dirname(__file__), "Bd_animes.db")

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

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS animes(
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
    #ruta_img = "C:/Users/villa/Downloads/ano.jpg"
    #db.agregar ("Another", ruta_img, "Latino", "1", "La historia se centra en una clase maldita y en los hilos del destino que llevan hasta a la muerte a todos los alumnos de la misma. Hace 26 años iba a esa clase una chica llamada Misaki. Buen deportista, popular, le caía bien a todo el mundo, sacaba las mejores notas... Pero un día murió dejando un vacío enorme en sus compañeros de clases. Estos, decididos a no olvidarla, siguieron actuando como si Misaki siguiera viva hasta la graduación.", "Temporada 1: 12 capitulos \n Ova: 1 \n Calidad: HD \n El anime se encuentra en pasfox, solo brinca 2 acortadores", "Sobrenatural", "https://pasfox.co/miYj", "")
    #db.eliminar( "Sousou No Frieren")
    #ruta_img = "C:/Users/villa/Downloads/frieren.jpg"
    #db.agregar ("Sousou No Frieren", ruta_img, "Sub-español", "1", "La maga Frieren formaba parte del grupo del héroe Himmel, quienes derrotaron al Rey Demonio tras un viaje de 10 años y devolvieron la paz al reino. Frieren es una elfa de más de mil años de vida, así que al despedirse de Himmel y sus compañeros promete que regresará para verlos y parte de viaje sola. Al cabo de cincuenta años, Frieren cumple su promesa y acude a visitar a Himmel y al resto.", "Temporada 1: 18 de 28 capitulos \n Calidad: MKV \n La temporada se encuentra en pasfox con un acordator en 4 capitulos", "Aventura", "https://pasfox.co/incXfp", "")