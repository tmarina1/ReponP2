
formulario1 = document.getElementById("formulario1");
formulario2 = document.getElementById("formulario2");
botonContinuar = document.getElementById("btn-continuar");

botonContinuar.addEventListener("click", this.mostrarFormulario2.bind(this));

function mostrarFormulario2(){
    formulario1.style.display = "none";
    formulario2.style.display = "block";
}
