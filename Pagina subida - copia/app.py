#pylint: disable=all
from flask import Flask, render_template, send_from_directory, g, request
import os
from Contenido import base_peliculas, base_juegos, base_series, base_animes, base_cursos
import base64
from flask_caching import Cache
import io
from PIL import Image

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def get_db_pelis():
    if 'db_pelis' not in g:  # Utiliza una clave diferente ('db_pelis') para la base de películas
        g.db_pelis = base_peliculas.Database_pelis()
    return g.db_pelis

def get_db_juegos():
    if 'db_juegos' not in g:  # Utiliza una clave diferente ('db_juegos') para la base de juegos
        g.db_juegos = base_juegos.Database_juego()
    return g.db_juegos

def get_db_series():
    if 'db_series' not in g:  # Utiliza una clave diferente ('db_series') para la base de series
        g.db_series = base_series.Database_series()
    return g.db_series

def get_db_animes():
    if 'db_animes' not in g:  # Utiliza una clave diferente ('db_animes') para la base de animes
        g.db_animes = base_animes.Database_animes()
    return g.db_animes

def get_db_cursos():
    if 'db_cursos' not in g:  # Utiliza una clave diferente ('db_animes') para la base de animes
        g.db_cursos = base_cursos.Database_cursos()
    return g.db_cursos

@app.teardown_appcontext
def teardown_db(error):
    db_pelis = getattr(g, 'dbpelis', None)
    if db_pelis is not None:
        db_pelis.conn.close()

    db_juegos = getattr(g, 'dbjuegos', None)
    if db_juegos is not None:
        db_juegos.conn.close()

    db_series = getattr(g, 'dbseries', None)
    if db_series is not None:
        db_series.conn.close()

    db_animes = getattr(g, 'dbanimes', None)
    if db_animes is not None:
        db_animes.conn.close()

    db_cursos = getattr(g, 'dbcursos', None)
    if db_cursos is not None:
        db_cursos.conn.close()

root_directory = os.path.dirname(os.path.abspath(__file__))

@app.route('/<path:filename>')
def custom_imd(filename):
    return send_from_directory(root_directory, filename)

@app.route('/')
@cache.cached(timeout=60)
def home():
    return render_template('index.html', message ='hola mundo')

@app.route('/animes', methods=['GET'])
def animes():

    db_animes = get_db_animes()
    number_page = int(request.args.get('page', 1))
    datos_pagina = 20
    genero_seleccionado = request.args.get('genero')
    buscar_por_nombre = request.args.get('nombre')

    if buscar_por_nombre:
        resultados_busqueda = db_animes.buscar(buscar_por_nombre)
    elif genero_seleccionado:
        resultados_busqueda = db_animes.filtrado(genero_seleccionado)
    else:
        resultados_busqueda = db_animes.paginacion(number_page, datos_pagina)

    animes_con_imagenes_base64 = []
    for anime in resultados_busqueda:

        imagen_bytes = anime[1]

        calidad_reducida = 45
        imagen_reducida_base64 = reducir_calidad_imagen(imagen_bytes, calidad_reducida)

        agg_img = (anime[0], imagen_reducida_base64, anime[2], anime[3], anime[4], anime[5], anime[6], anime[7])
        animes_con_imagenes_base64.append(agg_img)

    cantidad_animes = len(animes_con_imagenes_base64)
    return render_template('animes.html', animes=animes_con_imagenes_base64, number_page=number_page, datos_pagina=datos_pagina, cantidad_animes=cantidad_animes)

def precargar_datos():
    with app.app_context():
        db_animes = get_db_animes()
        datos_animes = db_animes.obtener_datos_animes()
        cache.set('datos_animes', datos_animes, timeout=3600)

        db_juegos = get_db_juegos()
        datos_juegos = db_juegos.obtener_datos_juegos()
        cache.set('datos_juegos', datos_juegos, timeout=3600)

        db_peliculas = get_db_pelis()
        datos_peliculas = db_peliculas.obtener_datos_peliculas()
        cache.set('datos_peliculas', datos_peliculas, timeout=3600)

        db_series = get_db_series()
        datos_series = db_series.obtener_datos_series()
        cache.set('datos_series', datos_series, timeout=3600)


@app.route('/juegos', methods=['GET'])
def juegos():
    db_juegos = get_db_juegos()
    number_page = int(request.args.get('page', 1))
    datos_pagina = 20
    genero_seleccionado = request.args.get('genero')
    buscar_por_nombre = request.args.get('nombre')

    if buscar_por_nombre:
        resultados_busqueda = db_juegos.buscar(buscar_por_nombre)
    elif genero_seleccionado:
        resultados_busqueda = db_juegos.filtrado(genero_seleccionado)
    else:
        resultados_busqueda = db_juegos.paginacion(number_page, datos_pagina)

    game_con_imagenes_base64 = []
    for games in resultados_busqueda:

        imagen_bytes = games[1]

        calidad_reducida = 45
        imagen_reducida_base64 = reducir_calidad_imagen(imagen_bytes, calidad_reducida)

        agg_img = (games[0], imagen_reducida_base64, games[2], games[3], games[4], games[5], games[6])
        game_con_imagenes_base64.append(agg_img)

    cantidad_juegos = len(game_con_imagenes_base64)
    return render_template('juegos.html', game=game_con_imagenes_base64, number_page=number_page, datos_pagina=datos_pagina, cantidad_juegos=cantidad_juegos)


def reducir_calidad_imagen(imagen_bytes, calidad_reducida):
    imagen_pil = Image.open(io.BytesIO(imagen_bytes))

    imagen_pil = imagen_pil.convert("RGB")

    buffer = io.BytesIO()
    imagen_pil.save(buffer, format="JPEG", quality=calidad_reducida)
    imagen_baja_calidad = buffer.getvalue()

    imagen_base64 = base64.b64encode(imagen_baja_calidad).decode('utf-8')

    return imagen_base64

@app.route('/peliculas', methods=['Get'])
def peliculas():
    db_pelis = get_db_pelis()
    number_page = int(request.args.get('page', 1))
    datos_pagina = 20
    genero_seleccionado = request.args.get('genero')
    buscar_por_nombre = request.args.get('nombre')

    if buscar_por_nombre:
        resultados_busqueda = db_pelis.buscar(buscar_por_nombre)
    elif genero_seleccionado:
        resultados_busqueda = db_pelis.filtrado(genero_seleccionado)
    else:
        resultados_busqueda = db_pelis.paginacion(number_page, datos_pagina)

    pelis_con_imagenes_base64 = []
    for peli in resultados_busqueda:
        imagen_bytes = peli[1]

        calidad_reducida = 45
        imagen_reducida_base64 = reducir_calidad_imagen(imagen_bytes, calidad_reducida)

        peli_con_imagenes_base64 = (peli[0], imagen_reducida_base64,peli[2], peli[3], peli[4], peli[5])
        pelis_con_imagenes_base64.append(peli_con_imagenes_base64)
    cantidad_pelis = len(pelis_con_imagenes_base64)
    return render_template('peliculas.html', pelis=pelis_con_imagenes_base64, number_page=number_page, datos_pagina=datos_pagina, cantidad_pelis=cantidad_pelis)

@app.route('/series', methods=['GET'])
def series():
    db_series = get_db_series()
    number_page = int(request.args.get('page', 1))
    datos_pagina = 20
    genero_seleccionado = request.args.get('genero')
    buscar_por_nombre = request.args.get('nombre')

    if buscar_por_nombre:
        resultados_busqueda = db_series.buscar(buscar_por_nombre)
    elif genero_seleccionado:
        resultados_busqueda = db_series.filtrado(genero_seleccionado)
    else:
        resultados_busqueda = db_series.paginacion(number_page, datos_pagina)

    series_con_imagenes_base64 = []
    for serie in resultados_busqueda:
        imagen_bytes = serie[1]

        calidad_reducida = 45
        imagen_reducida_base64 = reducir_calidad_imagen(imagen_bytes, calidad_reducida)

        agg_img = (serie[0], imagen_reducida_base64, serie[2], serie[3], serie[4], serie[5], serie[6], serie[7])

        series_con_imagenes_base64.append(agg_img)

    cantidad_series = len(series_con_imagenes_base64)
    return render_template('series.html', series=series_con_imagenes_base64, number_page=number_page, datos_pagina=datos_pagina, cantidad_series=cantidad_series)

@app.route('/cursos', methods=['GET'])
def cursos():
    db_cursos = get_db_cursos()
    number_page = int(request.args.get('page', 1))
    datos_pagina = 20
    genero_seleccionado = request.args.get('genero')
    buscar_por_nombre = request.args.get('nombre')

    if buscar_por_nombre:
        resultados_busqueda = db_cursos.buscar(buscar_por_nombre)
    elif genero_seleccionado:
        resultados_busqueda = db_cursos.filtrado(genero_seleccionado)
    else:
        resultados_busqueda = db_cursos.paginacion(number_page, datos_pagina)

    cursos_con_imagenes_base64 = []
    for curso in resultados_busqueda:
        imagen_bytes = curso[1]
        imagen_completa_base64 = base64.b64encode(imagen_bytes).decode('utf-8')

        buena = 50
        imagen_completa_base64 = reducir_calidad_imagen(imagen_bytes, buena)

        agg_img = (curso[0], imagen_completa_base64, curso[2], curso[3], curso[4])

        cursos_con_imagenes_base64.append(agg_img)
    cantidad_cursos = len(cursos_con_imagenes_base64)
    return render_template('cursos.html', cursos=cursos_con_imagenes_base64, number_page=number_page, datos_pagina=datos_pagina, cantidad_cursos=cantidad_cursos)


def get_details(content_type, element_name):
    db = None
    if content_type == 'peliculas':
        db = get_db_pelis()
    elif content_type == 'juegos':
        db = get_db_juegos()
    elif content_type == 'series':
        db = get_db_series()
    elif content_type == 'animes':
        db = get_db_animes()
    elif content_type == 'cursos':
        db = get_db_cursos()

    if db:
        detalles_contenido = db.obtener_detalles_elemento_seleccionado(element_name)
        detalles_contenido[f'imagen_{content_type}'] = base64.b64encode(detalles_contenido['imagen']).decode('utf-8')
        return render_template('informacion.html', detalles=detalles_contenido, tipo=content_type)
    else:
        return render_template('error.html')

@app.route('/informacion/<nombre_elemento>')
def detalles(nombre_elemento):
    tipo = request.args.get('tipo')
    return get_details(tipo, nombre_elemento)


if __name__ == '__main__':
    with app.app_context():
        precargar_datos()
    app.run(debug=True)