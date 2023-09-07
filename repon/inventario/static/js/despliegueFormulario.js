
formulario1 = document.getElementById("formulario1");
formulario2 = document.getElementById("formulario2");
botonContinuar = document.getElementById("btn-continuar");
botonVolver = document.getElementById("btn-volver");

botonContinuar.addEventListener("click", this.mostrarFormulario2.bind(this));
botonVolver.addEventListener("click", this.mostrarFormulario1.bind(this));

var mostrarFormulario2 = function(){
    formulario1.style.display = "none";
    formulario2.style.display = "block";
}

function mostrarFormulario1(){
    formulario2.style.display = "none";
    formulario1.style.display = "block";
}
