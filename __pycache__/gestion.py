import json
from datetime import datetime
#clase tarea
class tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False #hasta que nosotros no le demos una indicacion de que ya esta completado debe mantenerse
        #en false (sin completar)
    def marcar_completado(self):
        self.completado = True
    def editar_tarea(self, nuevo_titulo, nueva_descripcion, nueva_fecha):
        self.titulo = nuevo_titulo
        self.descripcion = nueva_descripcion
        self.fecha_vencimiento = nueva_fecha

class usuario:
    def __init__(self, nombre_usuario, contraseña):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.tareas = []
    def agregar_tarea(self,tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, titulo_tarea):
        self.tareas = [tarea for tarea in self.tareas if tarea.titulo != titulo_tarea]
#recorre toda la lista de tareas hasta llegar a que tenga el titulo al igual que al ingresado
    def obtener_tareas(self):
        return self.tareas
    