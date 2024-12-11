function activarbuscador() {
    // Obtener el input por su ID
    var input = document.getElementById('textbuscador');

    // Mostrar u ocultar el input alternando su estado
    if (input.style.display === 'none') {
        input.style.display = 'block'; // Mostrar el input al hacer clic en la imagen
    } else {
        input.style.display = 'none'; // Ocultar el input si ya está visible
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var paramet = new URLSearchParams(window.location.search);
    var tipo = paramet.get('tipo');

    if(tipo === 'peliculas') {
        document.getElementById("info_pelis").style.display = "block";
    } else if (tipo === 'juegos') {
        document.getElementById("info_juegos").style.display = "block"
    } else if (tipo === 'series') {
        document.getElementById("info_series").style.display = "block"
    } else if (tipo === 'animes') {
        document.getElementById("info_series").style.display = "block"
    } else if (tipo === 'cursos') {
        document.getElementById("info_cursos").style.display = "block"
    }
});

//#endregion
const enlacesDesplegables = document.querySelectorAll('.desplegable');

enlacesDesplegables.forEach((enlace) => {
    enlace.addEventListener('click', () => {
        const submenu = enlace.nextElementSibling;

        submenu.classList.toggle('visible');
    });
});

var mensajeCopia = document.getElementById("mensajeCopia");

function copiarAlPortapapeles() {
    // Selecciona el contenido del campo de entrada
    var inputContraseña = document.getElementById("inputContraseña");
    inputContraseña.select();

    // Copia el contenido al portapapeles
    document.execCommand("copy");

    // Deselecciona el campo de entrada
    window.getSelection().removeAllRanges();

    // Muestra el mensaje de éxito
    mensajeCopia.style.display = "flex";

    // Agrega la clase "mostrar" para activar la animación
    mensajeCopia.classList.add("mostrar");

    // Quita la clase "mostrar" después de 2 segundos para desencadenar la animación de salida
    setTimeout(function() {
        mensajeCopia.classList.remove("mostrar");
    }, 2500);
}


var mensajeCopias = document.getElementById("mensajeCopia");

function copiarAlPortapapeles() {
    // Selecciona el contenido del campo de entrada
    var inputContraseña = document.getElementById("inputContraseña");
    inputContraseña.select();

    // Copia el contenido al portapapeles
    document.execCommand("copy");

    // Deselecciona el campo de entrada
    window.getSelection().removeAllRanges();

    // Muestra el mensaje de éxito
    mensajeCopias.style.display = "flex";

    // Agrega la clase "mostrar" para activar la animación
    mensajeCopias.classList.add("mostrar");

    // Quita la clase "mostrar" después de 2 segundos para desencadenar la animación de salida
    setTimeout(function() {
        mensajeCopias.classList.remove("mostrar");
    }, 2500);
}


var mensajeCopia = document.getElementById("mensajeCopiaseries");

function copiarAlPortapapelesseries() {
    // Selecciona el contenido del campo de entrada
    var inputContraseña = document.getElementById("inputContraseñas");
    inputContraseña.select();

    // Copia el contenido al portapapeles
    document.execCommand("copy");

    // Deselecciona el campo de entrada
    window.getSelection().removeAllRanges();

    // Muestra el mensaje de éxito
    mensajeCopia.style.display = "flex";

    // Agrega la clase "mostrar" para activar la animación
    mensajeCopia.classList.add("mostrar");

    // Quita la clase "mostrar" después de 2 segundos para desencadenar la animación de salida
    setTimeout(function() {
        mensajeCopia.classList.remove("mostrar");
    }, 2500);
}