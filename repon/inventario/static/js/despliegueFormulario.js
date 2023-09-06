class DespliegueFormulario {
    constructor() {
        this.formulario1 = document.getElementById("formulario1");
        this.formulario2 = document.getElementById("formulario2");
        this.botonContinuar = document.getElementById("btn-continuar");

        this.botonContinuar.addEventListener("click", this.mostrarFormulario2.bind(this));
    }

    mostrarFormulario2() {
        this.formulario1.style.display = "none";
        this.formulario2.style.display = "block";
    }
}

export default DespliegueFormulario;
