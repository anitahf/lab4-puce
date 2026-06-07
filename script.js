const API_URL = "/api/tareas";

async function cargarTareas() {
    try {
        const respuesta = await fetch(API_URL);
        const tareas = await respuesta.json();

        const contenedor = document.getElementById("tareas");
        contenedor.innerHTML = "";

        let total = tareas.length;
        let completadas = tareas.filter(t => t.completada).length;
        let pendientes = total - completadas;

        document.getElementById("total").textContent = total;
        document.getElementById("pendientes").textContent = pendientes;
        document.getElementById("completadas").textContent = completadas;

        tareas.forEach(tarea => {
            const div = document.createElement("div");
            div.className = tarea.completada ? "tarea completada" : "tarea";

            div.innerHTML = `
                <div>
                    <h4>${tarea.titulo}</h4>
                    <p>${tarea.descripcion}</p>
                    <small>#${tarea.id}</small>
                </div>
                <div class="acciones">
                    <button onclick="completarTarea(${tarea.id})">✓</button>
                    <button onclick="eliminarTarea(${tarea.id})">🗑</button>
                </div>
            `;

            contenedor.appendChild(div);
        });

    } catch (error) {
        console.error("Error al cargar tareas:", error);
    }
}

async function crearTarea() {
    const titulo = document.getElementById("titulo").value;
    const descripcion = document.getElementById("descripcion").value;

    if (!titulo || !descripcion) {
        alert("Completa el título y la descripción");
        return;
    }

    const nuevaTarea = {
        titulo: titulo,
        descripcion: descripcion,
        completada: false
    };

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(nuevaTarea)
    });

    document.getElementById("titulo").value = "";
    document.getElementById("descripcion").value = "";

    cargarTareas();
}

async function completarTarea(id) {
    await fetch(`${API_URL}/${id}/completar`, {
        method: "PATCH"
    });

    cargarTareas();
}

async function eliminarTarea(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    cargarTareas();
}

cargarTareas();
