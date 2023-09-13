var formulario1 = document.getElementById("formulario1");
var formulario2 = document.getElementById("formulario2");
var botonContinuar = document.getElementById("btn-continuar");
var botonVolver = document.getElementById("btn-volver");

function mostrarFormulario2() {
    formulario1.style.display = "none";
    formulario2.style.display = "block";
}

function mostrarFormulario1() {
    formulario2.style.display = "none";
    formulario1.style.display = "block";
}

botonContinuar.addEventListener("click", mostrarFormulario2);
botonVolver.addEventListener("click", mostrarFormulario1);