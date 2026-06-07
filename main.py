from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="API Distribuida – Laboratorio IV",
    description="Gestión de tareas con operaciones CRUD completas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    completada: bool = False

tareas: List[Tarea] = [
    Tarea(id=1, titulo="Subir código a GitHub", descripcion="Repositorio lab4-puce con main.py, index.html y vercel.json", completada=False),
    Tarea(id=2, titulo="Conectar dominio a Vercel", descripcion="Configurar DNS y probar URL pública", completada=False),
    Tarea(id=3, titulo="Implementar búsqueda paralela", descripcion="ThreadPoolExecutor con 2, 4 y 8 hilos", completada=True),
    Tarea(id=4, titulo="Crear API REST con FastAPI", descripcion="Endpoints CRUD completos y CORS habilitado", completada=True)
]

@app.get("/")
def inicio():
    return {
        "mensaje": "API Distribuida - Laboratorio IV",
        "documentacion": "/docs",
        "endpoint_tareas": "/tareas"
    }

@app.get("/tareas")
def listar_tareas():
    return tareas

@app.post("/tareas", status_code=201)
def crear_tarea(tarea: Tarea):
    nuevo_id = max([t.id for t in tareas], default=0) + 1
    tarea.id = nuevo_id
    tareas.append(tarea)
    return {
        "mensaje": "Tarea creada exitosamente",
        "tarea": tarea
    }

@app.get("/tareas/{tarea_id}")
def obtener_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/tareas/{tarea_id}")
def actualizar_tarea(tarea_id: int, tarea_actualizada: Tarea):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            tarea_actualizada.id = tarea_id
            tareas[i] = tarea_actualizada
            return {
                "mensaje": "Tarea actualizada exitosamente",
                "tarea": tarea_actualizada
            }
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.patch("/tareas/{tarea_id}/completar")
def cambiar_estado_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea.id == tarea_id:
            tarea.completada = not tarea.completada
            return {
                "mensaje": "Estado de tarea actualizado",
                "tarea": tarea
            }
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int):
    for i, tarea in enumerate(tareas):
        if tarea.id == tarea_id:
            del tareas[i]
            return {
                "mensaje": "Tarea eliminada exitosamente"
            }
    raise HTTPException(status_code=404, detail="Tarea no encontrada")
